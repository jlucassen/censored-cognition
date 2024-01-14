import tiktoken
from openai import OpenAI

model = "gpt-4"

encoding = tiktoken.encoding_for_model(model)


logit_biases = {encoding.encode("3")[0]: -100}

print("logit_biases", logit_biases)

client = OpenAI()

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "Do your absolute best to fulfill the given task. Once you're done, please reason out loud about whether you completed the task correctly. Think how to solve it and the retry. Repeat until you are done.",
        },
        {"role": "user", "content": "Please count from 1 to 5."},
    ],
    temperature=0.9,
    max_tokens=512,
    top_p=0.98,
    frequency_penalty=0,
    presence_penalty=0,
    logit_bias=logit_biases,
    stream=True,
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(chunk.choices[0].delta.content, end="")
