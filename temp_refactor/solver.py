import backoff
import json
from openai import OpenAI
import logging
import os
import tiktoken

from sample import Sample

class Solver:
    '''
    Specifies runs.
    Init takes model and completion args.
    Solve takes a list of samples and returns a list of responses.
    '''
    def __init__(
            self,
            model: str,
            completion_args: dict = {}
    ):
        self.model = model
        self.completion_args = completion_args
        
        self.client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        self.encoding = tiktoken.encoding_for_model(self.model)

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
        return {'model':self.model, 'completion_args':self.completion_args}.__repr__()
        
    def solve(self, samples: [Sample]):
        responses = []
        for sample in samples:
            logit_biases = self.__censor_tokens(sample.censored_strings)
            response = self.complete_with_backoff(
                self.client,
                model=self.model,
                messages=sample.messages,
                logit_bias=logit_biases,
                #max_tokens=100,
                **self.completion_args)
            responses.append(response)
            print(response.choices[0].message.content)
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
    
    def complete_with_backoff(self, client, **kwargs):
        #@backoff.on_exception(backoff.expo, Exception, max_time=60)
        def complete():
            return client.chat.completions.create(**kwargs)
        return complete()