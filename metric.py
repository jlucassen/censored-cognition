import tiktoken
from openai import OpenAI
import os
import colorama

def report_success_LLM(response: str, task: str, print_output=True, model: str = 'gpt-4', reporter_prompt = None) -> bool:
    model = "gpt-4"
    client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

    default_reporter_prompt = "This is the output of a GPT-4 instance that was assigned a task. Your job is to report whether it completed that task successfully. Report your final answer by saying either <YES> or <NO>. The task was:\n"

    report = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": default_reporter_prompt+task if not reporter_prompt else reporter_prompt+task,
        },
        {"role": "user", "content": response}
    ],
    temperature=0.9,
    max_tokens=512,
    top_p=0.98,
    frequency_penalty=0,
    presence_penalty=0,
    stream=True,
    )

    if print_output: print(colorama.Fore.BLUE + '\n\nStarting LLM Report:\n\n')

    report_string = ''
    for chunk in report:
        content = chunk.choices[0].delta.content
        if content:
            report_string += chunk.choices[0].delta.content
            if print_output: print(chunk.choices[0].delta.content, end="", flush=True)

    if print_output: print(colorama.Style.RESET_ALL)

    if '<YES>' in report_string and '<NO>' not in report_string:
        return True
    elif '<NO>' in report_string and '<YES>' not in report_string:
        return False
    else:
        return None