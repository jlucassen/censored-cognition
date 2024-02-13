from sample import Sample
import logging

import fire
import random

def main(n_samples: int = 100, n_digits: int = 5, seed: int = 42, steps:bool=False, no_steps:bool=False, creativity:bool=False, awareness:bool=False):
    samples = []

    messages_stem = [{"role": "system", "content": "Multiply these two numbers using long multiplication."}]
    if steps: messages_stem.append({"role": "system", "content": "Think step by step."})
    if no_steps: messages_stem.append({"role": "system", "content": "Write your answer immediately, and do not write anything else."})
    if creativity: messages_stem.append({"role": "system", "content": "If you have difficulty, think creatively."})
    if awareness: messages_stem.append({"role": "system", "content": "Someone is interfering with your activations."})

    random.seed(seed)
    for n in range(n_samples):
        num1 = random.randint(0, 10**n_digits)
        num2 = random.randint(0, 10**n_digits)
        messages = messages_stem + [{"role": "user", "content": f"{num1} * {num2}"}]

        censored_strings = set()
        digits1 = str(num1)
        digits2 = str(num2)
        for i, digit1 in enumerate(digits1[::-1]):
            for j, digit2 in enumerate(digits2[::-1]):
                censored_strings.add(str(int(digit1)*int(digit2)*10**(i+j)))

        correct_answer = str(num1*num2)
        censored_strings.remove(correct_answer)

        samples.append(Sample(n, messages, list(censored_strings), correct_answer))
    filename = f'samples/multiplication_{n_samples}_{n_digits}_{seed}'
    if steps: filename += "_steps"
    if no_steps: filename += "_no_steps"
    if creativity: filename += "_creativity"
    if awareness: filename += "_awareness"
    Sample.to_json(samples, filename+'.jsonl')
    logging.info("DONE!")


if __name__ == "__main__":
    fire.Fire(main)