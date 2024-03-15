import random

from sample import Sample


def make_sample(n_samples: int = 100, n_digits: int = 5, seed: int = 42, uncensor:bool=False, oneShot:bool=False, steps:bool=False, creativity:bool=False, awareness:bool=False):
    samples = []

    messages_stem = [{"role": "user", "content": "Multiply these two numbers using long multiplication. Please conclude by saying the answer is _____."}]
    if oneShot: messages_stem.append({"role": "user", "content": "For example: 123 * 456. 3*6 = 18. 3*50 = 150. 3*400 = 1200. 20*6 = 120. 20*50 = 1000. 20*400 = 8000. 100*6 = 600. 100*50 = 5000. 100*400 = 40000. 18 + 150 + 1200 + 120 + 1000 + 8000 + 600 + 5000 + 40000 = 56088."})
    if steps: messages_stem.append({"role": "user", "content": "Think step by step."})
    if creativity: messages_stem.append({"role": "user", "content": "If you have difficulty, think creatively."})
    if awareness: messages_stem.append({"role": "user", "content": "Someone is interfering with your activations."})

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

        samples.append(Sample(n, messages, list(censored_strings) if not uncensor else [], correct_answer))
    filename = f'samples/multiplication/mult'
    if uncensor: filename += "_uncensor"
    if oneShot: filename += "_oneshot"
    if steps: filename += "_steps"
    if creativity: filename += "_creativity"
    if awareness: filename += "_awareness"
    filename += f"_{n_samples}_{n_digits}_{seed}"
    Sample.to_json(samples, filename+'.jsonl')

for i in range(1, 8):
    make_sample(1000, i, 42, uncensor=True)
    # make_sample(1000, i, 42, steps=True)
    # make_sample(1000, i, 42, creativity=True)
    # make_sample(1000, i, 42, awareness=True)
