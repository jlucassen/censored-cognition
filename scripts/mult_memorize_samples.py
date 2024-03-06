from sample import Sample

import random

def make_sample(n_samples: int = 100, n_digits: int = 5, seed: int = 42):
    samples = []

    random.seed(seed)
    for n in range(n_samples):
        if n == 0:
            lower = 0
        else:
            lower = 10**(n_digits-1)
        num1 = random.randint(lower, 10**n_digits)
        num2 = random.randint(lower, 10**n_digits)
        messages = [
            {"role":"system", "content":"Multiply these numbers in your head. Say only the answer."},
            {"role": "user", "content": f"{num1} * {num2} = "}]

        samples.append(Sample(n, messages, [], num1*num2))
    filename = f'samples/multiplication/mult_memorize_{n_samples}_{n_digits}_{seed}'
    Sample.to_json(samples, filename+'.jsonl')

for i in range(1, 8):
    make_sample(1000, i, 42)