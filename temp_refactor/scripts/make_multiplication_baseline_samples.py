from sample import Sample

import fire
import random

def main(n_samples: int = 100, n_digits: int = 5, seed: int = 42):
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
    filename = f'samples/multiplication_{n_samples}_{n_digits}_{seed}_baseline'
    Sample.to_json(samples, filename+'.jsonl')

if __name__ == "__main__":
    fire.Fire(main)

main(100, 1, 42)
main(100, 2, 42)
main(100, 3, 42)
main(100, 4, 42)
main(100, 5, 42)