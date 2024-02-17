from datetime import datetime
from openai import OpenAI
import os
import tiktoken
from tqdm import tqdm
import time

import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from sample import Sample
from result import SolverResult

class Solver:
    '''
    Specifies how to get a response from a model. Includes:
    - an id
    - a model string
    - a completion args dict
    
    Has functions to get SolverResponses from one Sample or a list of Samples.
    Init gets OpenAI api key from environment variable.
    Uses model embedding to turn censored strings into censored tokens.
    Has a repr that returns str(self.dict)
    Has some const solvers with common models and completion args.
    '''
    def __init__(
            self,
            model: str,
            completion_args: dict = {},
    ):
        self.model = model
        self.completion_args = completion_args

        self.log_filename = datetime.now().strftime('logs/solver_results/solver_result_log_%Y_%m_%d_%H%M%S.txt')
        open(self.log_filename, "w")
        
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.encoding = tiktoken.encoding_for_model(self.model)

        self.lock = threading.Lock()
        self.rpm = 500

    def __repr__(self):
        return str(self.__dict__)
        
    def solve_sample(self, sample: Sample, pbar=None) -> SolverResult:
        time.sleep(60/self.rpm) # respect requests per minute limit
        logit_biases = self.__censor_tokens(sample.censored_strings)
        response = self.complete_with_modifiers(
            self.client,
            model=self.model,
            messages=sample.messages,
            logit_bias=logit_biases,
            stream=True,
            **self.completion_args)
        
        full_response = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content

        result = SolverResult(sample, self, full_response)
        with self.lock:
            with open(self.log_filename, 'a') as logfile:
                logfile.write(result.__repr__() + "\n")
            if pbar is not None:
                pbar.update(1)
        return result
    
    def solve_samples(self, samples:list[Sample], num_threads = 10) -> list[SolverResult]:
        if num_threads > 1:
            with tqdm(total=len(samples)) as pbar:
                curried_solve_sample = partial(self.solve_sample, pbar=pbar)

                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    responses = executor.map(curried_solve_sample, samples)
            responses = list(responses)
        else:
            responses = []
            for sample in tqdm(samples):
                responses.append(self.solve_sample(sample))
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
    
    def complete_with_modifiers(self, client, **kwargs):
        def complete():
            return client.chat.completions.create(**kwargs)
        return complete()
    
GPT_3_STRING = 'gpt-3.5-turbo-0125'
GPT_4_STRING = 'gpt-4-0125-preview'