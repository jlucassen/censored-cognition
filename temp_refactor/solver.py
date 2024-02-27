from datetime import datetime
from openai import OpenAI
import os
import tiktoken
from tqdm import tqdm
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from sample import Sample

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
        return str({'model': self.model, 'completion_args': self.completion_args})
        
    def solve_sample(self, sample: Sample, pbar=None):
        time.sleep(60/self.rpm) # respect requests per minute limit
        logit_biases = self.__censor_tokens(sample.censored_strings)
        response = self.complete_with_modifiers(
            self.client,
            model=self.model,
            messages=sample.messages,
            logit_bias=logit_biases,
            #stream=True,
            **self.completion_args)
        
        # non-streaming
        full_response = response.choices[0].message.content

        # streaming
        # full_response = ""
        # for chunk in response:
        #     content = chunk.choices[0].delta.content
        #     if content:
        #         full_response += content

        result = SolverResult(sample, self, full_response)
        with self.lock:
            with open(self.log_filename, 'a') as logfile:
                logfile.write(result.__repr__() + "\n")
            if pbar is not None:
                pbar.update(1)
        return result
    
    def solve_samples(self, samples:list[Sample], num_threads = 10):
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

def get_gpt_4_string():
    real_gpt_4_string = 'gpt-4-0125-preview'
    print("USING GPT-4. THIS MIGHT BE EXPENSIVE, ARE YOU SURE?")
    print("Type 'Y' to continue, '3' to use GPT-3, or anything else to cancel.")
    user_input = input()
    if user_input == 'Y':
        print("Using "+real_gpt_4_string)
        return real_gpt_4_string
    elif user_input == '3':
        print("Using "+GPT_3_STRING)
        return GPT_3_STRING
    else:
        raise Exception("Run cancelled. Exception data: LMAO POOR")
GPT_4_STRING = get_gpt_4_string()

class SolverResult:
    def __init__(
            self,
            sample,
            solver,
            response: str,
    ):
        self.sample = sample
        self.response = response
        self.solver = solver

        if isinstance(self.sample, dict):
            self.sample = Sample(**self.sample)
        if isinstance(self.solver, dict):
            self.solver = Solver(**self.solver)

    def __repr__(self):
        return str(self.__dict__)
    
    @classmethod
    def from_json(self, path: str):
        with open(path, "r") as f:
            lines = [json.loads(line) for line in f.readlines()]
            return [SolverResult(**solver_result) for solver_result in lines]
        
    @classmethod
    def to_json(self, solver_results: list, path: str):
        with open(path, "w") as f:
            for solver_result in solver_results:
                f.write((solver_result.__repr__() + "\n").replace("'", '"'))