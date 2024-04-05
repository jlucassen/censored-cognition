import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial

from tqdm import tqdm

from .sample import Sample
from .solver import Solver, SolverResult


class Judge:
    """
    Specifies how to judge a solver's response. Includes:
    - an id
    - a judge function, SolverResult -> JudgeResult

    Has a function to batch judging function over a list of solver results.
    Has a repr that returns str(self.dict)
    Has some const judges with common judge functions.
    """

    def __init__(self, id, judge_function_name: str, logging=True):
        self.id = id
        self.judge_function_name = judge_function_name

        self.logging = logging
        if logging:
            self.log_filename = datetime.now().strftime(
                "logs/all_runs/judge_results/judge_result_log_%Y_%m_%d_%H%M%S.txt"
            )
            open(self.log_filename, "w")

        self.lock = threading.Lock()
        self.rpm = 10000

    def judge_solver_result(self, solver_result, pbar=None):
        time.sleep(60 / self.rpm)  # respect requests per minute limit
        assert isinstance(solver_result, SolverResult)
        judge_bool = judge_func_names_to_funcs[self.judge_function_name](solver_result)
        judge_result = JudgeResult(
            solver_result.sample,
            solver_result.solver,
            self,
            solver_result.response,
            judge_bool,
        )
        with self.lock:
            if self.logging:
                with open(self.log_filename, "a") as logfile:
                    logfile.write(judge_result.__repr__() + "\n")
            if pbar is not None:
                pbar.update(1)
        return judge_result

    def judge_solver_results(self, solver_results, num_threads=10):
        assert isinstance(solver_results, list)
        if num_threads > 1:
            with tqdm(total=len(solver_results)) as pbar:
                curried_judge_solver_result = partial(
                    self.judge_solver_result, pbar=pbar
                )
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    judge_results = list(
                        executor.map(
                            lambda solver_result: curried_judge_solver_result(
                                solver_result
                            ),
                            solver_results,
                        )
                    )
            judge_results = list(judge_results)
        else:
            judge_results = []
            for solver_result in tqdm(solver_results):
                judge_results.append(self.judge_solver_result(solver_result))
        return judge_results

    def __repr__(self):
        return str({"id": self.id, "judge_function_name": self.judge_function_name})


def contains_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) in str(solver_response.response)


def equals_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) == str(solver_response.response)


def contains_digit_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) in str(
        solver_response.response.replace(",", "")
    )


def equals_digit_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) == str(
        solver_response.response.replace(",", "")
    )


CONTAINS_FUNC = "contains"
EQUALS_FUNC = "equals"
CONTAINS_DIGIT_FUNC = "contains_digit"
EQUALS_DIGIT_FUNC = "equals_digit"

judge_func_names_to_funcs = {
    CONTAINS_FUNC: contains_judge_func,
    CONTAINS_DIGIT_FUNC: contains_digit_judge_func,
    EQUALS_FUNC: equals_judge_func,
    EQUALS_DIGIT_FUNC: equals_digit_judge_func,
}

CONTAINS_JUDGE = Judge(0, CONTAINS_FUNC)
EQUALS_JUDGE = Judge(1, EQUALS_FUNC)
CONTAINS_DIGIT_JUDGE = Judge(2, CONTAINS_DIGIT_FUNC)
EQUALS_DIGIT_JUDGE = Judge(3, EQUALS_DIGIT_FUNC)


class JudgeResult:
    def __init__(
        self, sample, solver, judge, response: str, correct: bool, logging=True
    ):
        self.sample = sample
        self.response = response
        self.solver = solver
        self.judge = judge
        self.correct = correct

        if isinstance(self.sample, dict):
            self.sample = Sample(**self.sample)
        if isinstance(self.solver, dict):
            self.solver = Solver(**self.solver, logging=logging)

    def __repr__(self):
        return str(self.__dict__)
