import datetime
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import inflect

from solver import Solver, SolverResult
from utils import load_jsonl

LOGS_DIR = Path("logs")


@dataclass
class Sample:
    id: int
    task: str
    censored_numbers: [int]
    correct_answer: int


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
        try:
            correct = int(response.strip()) == sample.correct_answer
        except ValueError as e:
            correct = False

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
        # censor all weird number representations
        # probably we should have censored only ones in the `numbers` but might as well
        censored_strings += [chr(number) for number in range(120782, 120831 + 1)]
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
            "correct_answer": sample.correct_answer,
        }

        with self.lock:
            with open(self.log_filename, "a+", encoding="utf-8") as log_file:
                log_file.write(json.dumps(log_dict, ensure_ascii=False) + "\n")

    def run(self, solver: Solver, num_threads: int = 10):
        samples = [sample | {"id": i} for i, sample in enumerate(load_jsonl(self.path_to_samples))]
        samples = [Sample(**sample) for sample in samples for _ in range(self.upsample)]
        print("Running on N samples:", len(samples))

        def curried_evaluate(sample):
            self.evaluate_sample(solver, sample)

        run_spec = {
            "solver": solver.name,
            "num_threads": num_threads,
            "upsample": self.upsample,
            "task_path": self.path_to_samples,
        }
        with open(self.log_filename, "a+", encoding="utf-8") as log_file:
            log_file.write(json.dumps(run_spec) + "\n")

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

        metrics = {
            "correct_count": correct_count,
            "correct_percent": correct_percent,
            "unsure_count": unsure_count,
            "type": "metrics",
        }

        with open(self.log_filename, "a+", encoding="utf-8") as log_file:
            log_file.write(json.dumps(metrics) + "\n")
