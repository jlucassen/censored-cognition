import logging
from dataclasses import dataclass

import tiktoken
import yaml
from openai import OpenAI

from utils import complete_with_backoff

DEFAULT_COMPLETION_ARGS = {
    "temperature": 0.9,
    "max_tokens": 256,
    "top_p": 0.98,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

DEFAULT_ANSWER_FORMATTING_INSTRUCTION = """When you're done, write the answer as "\nAnswer: <answer>", including just the final result without any reasoning. The final <answer> must be an integer. It will be parsed by Python, so it will raise an error if it's not an integer. For example, if the answer is 42, write '\nAnswer: 42'"""


@dataclass
class SolverResult:
    answer: str
    full_completion: str


class Solver:
    def __init__(
        self,
        name: str,
        model: str,
        base_prompt: str,
        use_token_hint: bool = False,
        completion_args: dict = {},
        formatting_instruction: str = DEFAULT_ANSWER_FORMATTING_INSTRUCTION,
    ):
        self.name = name
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.client = OpenAI()

        self.base_prompt = base_prompt
        self.use_token_hint = use_token_hint
        self.completion_args = DEFAULT_COMPLETION_ARGS | completion_args
        self.formatting_instruction = formatting_instruction

    @classmethod
    def from_yaml(self, path: str):
        with open(path, "r") as f:
            config = yaml.safe_load(f)

        return Solver(**config)

    def solve(self, task: str, censored_strings: list[str] = []) -> SolverResult:
        # censor model's cognition
        logit_biases = self.censor_strings(censored_strings)

        # construct system prompt
        system_prompt = self.base_prompt + self.formatting_instruction
        if self.use_token_hint:
            max_tokens = self.completion_args["max_tokens"]
            token_hint = f"Note: You have a total of {max_tokens} tokens (about {max_tokens * 0.75//1}) to complete the task."
            system_prompt += "\n\n" + token_hint

        # construct prompt
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        response = complete_with_backoff(
            self.client,
            model=self.model,
            messages=messages,
            logit_bias=logit_biases,
            **self.completion_args,
        )
        response_text = response.choices[0].message.content
        answer = self.extract_answer(response_text)
        return SolverResult(answer=answer, full_completion=response_text)

    def extract_answer(self, response: str) -> str:
        """
        Extracts the answer from the response.
        """
        # extract answer from response
        answer = response.split("Answer:")[-1]
        answer = answer.strip()
        return answer

    def censor_strings(self, strings: list[str]) -> dict[str, int]:
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

        logging.debug(f"Censored tokens: {censored_tokens}")
        logging.debug(f"Logit biases: {logit_biases}")
        return logit_biases
