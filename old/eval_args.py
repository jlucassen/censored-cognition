from dataclasses import dataclass
import tiktoken
from openai import OpenAI
import os

@dataclass
class EvalArgs():
    model: str
    task: str
    censored_tokens: [str]
    help_content: str
    model_kwargs: dict

def eval_with_args(args: EvalArgs, print_output=True) -> str:
    '''
    Input: an EvalArgs with all the info needed to specify an OpenAI call, run the call (and optional print flag).
    Output: result string.
    '''
    encoding = tiktoken.encoding_for_model(args.model)
    logit_biases = {encoding.encode(token)[0]: -100 for token in args.censored_tokens}
    client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
    model=args.model,
    messages=[
        {
            "role": "system",
            "content": args.help_content,
        },
        {"role": "user", "content": args.task}
    ],
    logit_bias=logit_biases,
    stream=True,
    **args.model_kwargs
    )

    response_string = ''
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            response_string += chunk.choices[0].delta.content
            if print_output: print(chunk.choices[0].delta.content, end="", flush=True)

    return response_string