import datetime
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import inflect

from metric import evaluate_response
from solver import Solver, SolverResult
from utils import load_jsonl

LOGS_DIR = Path("logs")


@dataclass
class Sample:
    id: int
    task: str
    censored_numbers: [str]


class CensoredCognition:
    def __init__(self, path_to_samples: str, upsample: int = 10):
        self.sample_metrics = []
        self.path_to_samples = path_to_samples
        self.upsample = upsample

        current_time = datetime.datetime.now()
        self.log_filename = LOGS_DIR / f"log_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.jsonl"
        self.lock = threading.Lock()

    def evaluate_sample(self, solver: Solver, sample: Sample):
        task = sample.task  # e.g. "Compute the result of 4 + 7."
        censored_strings = self.censor_numbers(
            sample.censored_numbers
        )  # e.g. ["4", "four", " four", "Four", " Four"]

        result = solver.solve(task=task, censored_strings=censored_strings)
        response = result.answer
        correct = evaluate_response(response, task)
        self.log_result(sample, result, correct)

        self.sample_metrics.append(
            {
                "task": task,
                "result": result,
                "correct": correct,
            }
        )

    def censor_numbers(self, numbers: [int]) -> list[str]:
        """
        Input: a list of numbers to censor.
        Output: a list of strings to censor, with alternate representations of those numbers.
        """
        inflector = inflect.engine()

        censored_strings = []
        censored_strings += [str(number) for number in numbers]  # censor string digits
        censored_strings += [
            inflector.number_to_words(number) for number in numbers
        ]  # censor lowercase English
        censored_strings += [
            inflector.number_to_words(number).capitalize() for number in numbers
        ]  # censor uppercase English
        censored_strings += [" " + cs for cs in censored_strings]

        return censored_strings

    def log_result(self, sample: Sample, result: SolverResult, correct: Optional[bool]):
        log_dict = {
            "sample": sample.__dict__,
            "result": result.__dict__,
            "correct": correct,
        }

        with self.lock:
            with open(self.log_filename, "a+", encoding="utf-8") as log_file:
                log_file.write(json.dumps(log_dict, ensure_ascii=False) + "\n")

    def run(self, solver: Solver, num_threads: int = 10):
        samples = [sample | {"id": i} for i, sample in enumerate(load_jsonl(self.path_to_samples))]
        print("Loaded unique samples:", len(samples))
        samples = [Sample(**sample) for sample in samples for _ in range(self.upsample)]
        print("Upsampled samples:", len(samples))

        def curried_evaluate(sample):
            self.evaluate_sample(solver, sample)

        print("Writing logs to", self.log_filename)
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(curried_evaluate, samples)

        correct_count = sum(
            [1 if metric["correct"] == True else 0 for metric in self.sample_metrics]
        )
        unsure_count = sum(
            [1 if metric["correct"] == None else 0 for metric in self.sample_metrics]
        )

        correct_percent = correct_count / len(self.sample_metrics)
        unsure_count = unsure_count / len(self.sample_metrics)

        print(f"Successful: {correct_count} ({correct_percent:.2%})")
        print(f"Unsure: {unsure_count}")
