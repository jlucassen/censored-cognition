import json
import random
from typing import Tuple

import fire


def write_to_jsonl(path: str, data: list):
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def get_random_task(max_num: int, censor_answer: bool, seed: int) -> Tuple[str, list[int]]:
    rng = random.Random(seed)
    a, b = rng.randint(1, max_num), rng.randint(1, max_num)
    answer = a + b
    task_str = f"Compute the result of {a} + {b}."
    censored_numbers = [a, b]
    if censor_answer:
        censored_numbers.append(answer)
    return task_str, censored_numbers


def main(n_samples: int = 100, max_num: int = 20, censor_answer: bool = True, seed: int = 42):
    data = []
    tuples = set()
    i = 0
    while len(data) < n_samples:
        task_str, numbers = get_random_task(
            max_num=max_num, censor_answer=censor_answer, seed=seed + i
        )
        i += 1

        if tuple(numbers) in tuples:
            continue
        else:
            tuples.add(tuple(numbers))

        data.append(
            {
                "id": i,
                "censored_numbers": numbers,
                "task": task_str,
            }
        )

    file_name = "sum_2_ints"
    if censor_answer:
        file_name += "_censored_answer"
    write_to_jsonl(f"data/{file_name}.jsonl", data)


if __name__ == "__main__":
    fire.Fire(main)
