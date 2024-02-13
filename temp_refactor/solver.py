from datetime import datetime
import json
from openai import OpenAI
import os
import tiktoken
from tqdm import tqdm
import time
import backoff
import timeout_decorator

import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from sample import Sample
from result import Result
from judge import Judge

class Solver:
    '''
    Specifies runs.
    Init takes model and completion args.
    Solve takes a list of samples and returns a list of responses.
    '''
    def __init__(
            self,
            model: str,
            completion_args: dict = {},
            do_log: bool = True,
            do_print: bool = False
    ):
        self.model = model
        self.completion_args = completion_args
        self.do_log = do_log
        self.do_print = do_print

        if do_log:
            self.log_filename = datetime.now().strftime('logs/log_%Y_%m_%d_%H%M%S.txt')
            open(self.log_filename, "w")
        
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.encoding = tiktoken.encoding_for_model(self.model)

        self.lock = threading.Lock()
        self.rpm = 500
        

    @classmethod
    def to_json(self, solvers:list, path:str):
        with open(path, "w") as f:
            for solver in solvers:
                f.write((solver.__repr__() + "\n").replace("'", '"'))


    @classmethod
    def from_json(self, path: str):
        with open(path, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            return [Solver(**solver) for solver in lines]

    def __repr__(self):
        return str(self.__dict__)
        
    def solve_sample(self, sample: Sample, judge: Judge, temp=0, max_tokens=100, pbar=None):
        time.sleep(60/self.rpm) # respect requests per minute limit
        logit_biases = self.__censor_tokens(sample.censored_strings)
        response = self.complete_with_timeout(
            self.client,
            model=self.model,
            messages=sample.messages,
            logit_bias=logit_biases,
            temperature=temp,
            max_tokens=max_tokens,
            stream=True,
            **self.completion_args)
        
        if response is None:
            return Result(sample, "", False, False)
        
        full_response = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                if self.do_print:
                    print(content, end="", flush=True)
        correct = judge.bool_judge(sample, full_response)

        result = Result(sample, full_response, correct)
        if self.do_log:
            with self.lock:
                with open(self.log_filename, 'a') as logfile:
                    logfile.write(result.__repr__() + "\n")
        if pbar is not None:
            with self.lock:
                pbar.update(1)
        return result

    
    def solve_samples(self, samples:list[Sample], judge: Judge, num_threads = 10, temp=0, max_tokens=100):
        print(f"{num_threads=}")
        if num_threads > 1:
            with tqdm(total=len(samples)) as pbar:
                curried_solve_sample = partial(self.solve_sample, judge=judge, temp=temp, max_tokens=max_tokens, pbar=pbar)

                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    responses = executor.map(curried_solve_sample, samples)
            responses = list(responses)
        else:
            responses = []
            for sample in tqdm(samples):
                responses.append(self.solve_sample(sample, judge, temp, max_tokens))

        return responses

    def __censor_tokens(self, strings: list[str]) -> dict[str, int]:
        logit_biases = {}
        space_encoding = self.encoding.encode(" ")[0]
        censored_tokens = []
        for string in strings:
            tokens = self.encoding.encode(string)
            tokens = [token for token in tokens if token != space_encoding]
            decoded_tokens = [self.encoding.decode([token]) for token in tokens]
            if len(decoded_tokens) > 1:
                censored_tokens += decoded_tokens
            for token in tokens:
                logit_biases[token] = -100
        return logit_biases
    
    def complete_with_timeout(self, client, **kwargs):
        #@backoff.on_exception(backoff.expo, Exception, max_time=60)
        @timeout_decorator.timeout(5)
        def complete():
            return client.chat.completions.create(**kwargs)
        
        try:
            v = complete()
            print('no timeout!')
            return v
        except TimeoutError:
            print('timeout!')
            return None