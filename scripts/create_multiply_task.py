import json
import random
from math import prod
from typing import Tuple

import fire


def write_to_jsonl(path: str, data: list):
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")


def get_random_task(
    nums: int = 5, max_num: int = 20, censor_answer: bool = True, seed: int = 42
) -> Tuple[str, list[int], int]:
    rng = random.Random(seed)
    numbers = [rng.randint(1, max_num) for _ in range(nums)]
    answer = prod(numbers)
    numbers_str = [str(number) for number in numbers]
    task_str = f"Compute the result of {' * '.join(numbers_str)}."
    censored_numbers = numbers.copy()
    if censor_answer:
        censored_numbers.append(answer)
    return task_str, censored_numbers, answer


def main(
    n_samples: int = 100,
    n_nums: int = 5,
    max_num: int = 20,
    censor_answer: bool = True,
    seed: int = 42,
):
    data = []
    tuples = set()
    i = 0
    while len(data) < n_samples:
        task_str, numbers, answer = get_random_task(
            nums=n_nums, max_num=max_num, censor_answer=censor_answer, seed=seed + i
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
                "correct_answer": answer,
            }
        )

    file_name = f"prod_{n_nums}_ints_1to{max_num}"
    if censor_answer:
        file_name += "_censored_answer"
    write_to_jsonl(f"data/{file_name}.jsonl", data)


if __name__ == "__main__":
    fire.Fire(main)
