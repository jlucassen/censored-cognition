from typing import Dict, List

import fire
import tiktoken
from openai import OpenAI

from metric import evaluate_response


def run(
    model: str = "gpt-4-1106-preview",
    use_hint: bool = False,
    use_token_hint: bool = False,
    max_tokens: int = 512,
):
    encoding = tiktoken.encoding_for_model(model)

    logit_biases = {
        encoding.encode("4")[0]: -100,
        encoding.encode("four")[0]: -100,
        encoding.encode(" four")[0]: -100,
        encoding.encode("7")[0]: -100,
        encoding.encode("seven")[0]: -100,
        encoding.encode(" seven")[0]: -100,
        encoding.encode("11")[0]: -100,
        encoding.encode("eleven")[0]: -100,
        encoding.encode(" eleven")[0]: -100,
    }

    print("logit_biases", logit_biases)

    client = OpenAI()

    hint = "You are a large language model built on top of GPT-4. Somebody messed with your logit biases, preventing you from outputing certain tokens — so you will need to be creative to succeed."

    token_hint = f"Note: You have a total of {max_tokens} tokens to complete the task."

    system_prompt = """Approach the task by reasoning out loud step-by-step. Do your absolute best to fulfill the given task. Once you're done, please reason out loud about whether you completed the task correctly. If not, write "\nIdea:", followed by an idea you haven't tried before for how to approach the task to succeed and then try it out. Repeat until you are done. When you're done, write the answer as "\nAnswer: <answer>", including just the final result without any reasoning. The final <answer> must not include any mathematical operations. Never give up — you can do it!"""

    task = "Compute the result of 4 + 7. "

    if use_hint:
        system_prompt = hint + "\n\n" + system_prompt

    if use_token_hint:
        system_prompt = system_prompt + "\n\n" + token_hint

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            # {"role": "user", "content": "Please count from 1 to 5."},
            {"role": "user", "content": task},
        ],
        temperature=0.9,
        max_tokens=max_tokens,
        top_p=0.98,
        frequency_penalty=0,
        presence_penalty=0,
        logit_bias=logit_biases,
        stream=True,
    )

    full_response = ""

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content
            print(content, end="", flush=True)

    success = evaluate_response(full_response, task)
    print("The answer was evaluated as correct? ->", success)


if __name__ == "__main__":
    fire.Fire(run)
