from datetime import datetime
import time
from tqdm import tqdm

import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from result import SolverResult, JudgeResult

class Judge:
    '''
    Specifies how to judge a solver's response. Includes:
    - an id
    - a judge function, SolverResult -> JudgeResult
    
    Has a function to batch judging function over a list of solver results.
    Has a repr that returns str(self.dict)
    Has some const judges with common judge functions.
    '''
    def __init__(self, id, judge_function:callable):
        self.id = id
        self.judge_function = judge_function

        self.log_filename = datetime.now().strftime('logs/judge_results/judge_result_log_%Y_%m_%d_%H%M%S.txt')
        open(self.log_filename, "w")

        self.lock = threading.Lock()
        self.rpm = 500

    def judge_solver_result(self, solver_result, pbar=None):
        time.sleep(60/self.rpm) # respect requests per minute limit
        assert isinstance(solver_result, SolverResult)
        judge_bool = self.judge_function(solver_result)
        judge_result = JudgeResult(solver_result.sample, solver_result.solver, self, solver_result.response, judge_bool)
        with self.lock:
            with open(self.log_filename, 'a') as logfile:
                logfile.write(judge_result.__repr__()+"\n")
            if pbar is not None:
                pbar.update(1)
        return judge_result

    def judge_solver_results(self, solver_results, num_threads = 10):
        assert isinstance(solver_results, list)
        if num_threads > 1:
            with tqdm(total=len(solver_results)) as pbar:
                curried_judge_solver_result = partial(self.judge_solver_result, pbar=pbar)
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    judge_results = list(executor.map(lambda solver_result: curried_judge_solver_result(solver_result), solver_results))
            judge_results = list(judge_results)
        else:
            judge_results = []
            for solver_result in tqdm(solver_results):
                judge_results.append(self.judge_solver_result(solver_result))
        return judge_results
    
    def __repr__(self):
        return str({'id': self.id, 'judge_function_name': self.judge_function.__name__})

def contains_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) in str(solver_response.response)
CONTAINS_JUDGE = Judge(0, contains_judge_func)
def equals_judge_func(solver_response):
    return str(solver_response.sample.correct_answer) == str(solver_response.response)
EQUALS_JUDGE = Judge(1, equals_judge_func)
def contains_digit_judge_func(solver_response):
    digit_substring = ''.join([i for i in solver_response.response if i.isdigit()])
    return str(digit_substring) in str(solver_response.response)
CONTAINS_DIGIT_JUDGE = Judge(2, contains_digit_judge_func)
def equals_digit_judge_func(solver_response):
    digit_substring = ''.join([i for i in solver_response.response if i.isdigit()])
    return str(digit_substring) == str(solver_response.response)
EQUALS_DIGIT_JUDGE = Judge(3, equals_digit_judge_func)