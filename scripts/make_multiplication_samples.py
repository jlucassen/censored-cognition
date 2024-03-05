from sample import Sample

import random

def make_sample(n_samples: int = 100, n_digits: int = 5, seed: int = 42, steps:bool=False, creativity:bool=False, awareness:bool=False, folder=""):
    samples = []

    messages_stem = [{"role": "system", "content": "Multiply these two numbers using long multiplication."}]
    if steps: messages_stem.append({"role": "system", "content": "Think step by step."})
    if creativity: messages_stem.append({"role": "system", "content": "If you have difficulty, think creatively."})
    if awareness: messages_stem.append({"role": "system", "content": "Someone is interfering with your activations."})

    random.seed(seed)
    for n in range(n_samples):
        if n == 0:
            lower = 0
        else:
            lower = 10**(n_digits-1)
        num1 = random.randint(lower, 10**n_digits)
        num2 = random.randint(lower, 10**n_digits)
        messages = messages_stem + [{"role": "user", "content": f"{num1} * {num2}"}]

        censored_strings = set()
        digits1 = str(num1)
        digits2 = str(num2)
        for i, digit1 in enumerate(digits1[::-1]): 
            for j, digit2 in enumerate(digits2[::-1]):
                censored_strings.add(str(int(digit1)*int(digit2)*10**(i+j))) # digit1*digit2
        for i, digit1 in enumerate(digits1[::-1]): 
            censored_strings.add(str(int(digit1)*num2*10**i)) # digit1*num2
        for j, digit2 in enumerate(digits2[::-1]):
            censored_strings.add(str(int(digit2)*num1*10**j)) # num1*digit2

        correct_answer = str(num1*num2)
        if correct_answer in censored_strings: censored_strings.remove(correct_answer)

        samples.append(Sample(n, messages, list(censored_strings), correct_answer))
    filename = f'samples/{folder + "/" if folder else ""}multiplication_{n_samples}_{n_digits}_{seed}'
    if steps: filename += "_steps"
    if creativity: filename += "_creativity"
    if awareness: filename += "_awareness"
    Sample.to_json(samples, filename+'.jsonl')

for i in range(1, 8):
    make_sample(1000, i, 42, folder="multiplication")
    make_sample(1000, i, 42, steps=True, folder="multiplication_steps")
    make_sample(1000, i, 42, creativity=True, folder="multiplication_creativity")
    make_sample(1000, i, 42, awareness=True, folder="multiplication_awareness")