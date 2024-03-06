from sample import Sample
from solver import Solver, get_gpt_3_string, get_gpt_4_string, SolverResult
from judge import CONTAINS_DIGIT_JUDGE, JudgeResult

import matplotlib.pyplot as plt
import numpy as np

gpt_3_string = get_gpt_3_string()
gpt_4_string = get_gpt_4_string()

samples_1 = Sample.from_json('samples/multiplication/mult_memorize_1000_1_42.jsonl')
samples_3 = Sample.from_json('samples/multiplication/mult_memorize_1000_3_42.jsonl')
samples_2 = Sample.from_json('samples/multiplication/mult_memorize_1000_2_42.jsonl')
samples_4 = Sample.from_json('samples/multiplication/mult_memorize_1000_4_42.jsonl')
samples_5 = Sample.from_json('samples/multiplication/mult_memorize_1000_5_42.jsonl')
samples_6 = Sample.from_json('samples/multiplication/mult_memorize_1000_6_42.jsonl')
samples_7 = Sample.from_json('samples/multiplication/mult_memorize_1000_7_42.jsonl')

solver_4 = Solver(gpt_3_string, {'temperature': 0.0, 'max_tokens': 30, 'seed': 42})
solver_3 = Solver(gpt_4_string, {'temperature': 0.0, 'max_tokens': 30, 'seed': 42})

solver_results_3 = []
solver_results_4 = []

for i, samples in enumerate([samples_1, samples_2, samples_3, samples_4, samples_5 , samples_6, samples_7]):
    print(f'Solving samples with {i+1} digits with gpt-3')
    solver_3.completion_args['max_tokens'] = int(2*(i+1)*4/3+5) # i+1 digits, 2 numbers, 4/3 characters per digit w commas, 5 for good measure
    solution_3 = solver_3.solve_samples(samples, num_threads=100)
    print(f'Solving samples with {i+1} digits with gpt-4')
    solver_4.completion_args['max_tokens'] = int(2*(i+1)*4/3+5) # i+1 digits, 2 numbers, 4/3 characters per digit w commas, 5 for good measure
    solution_4 = solver_4.solve_samples(samples, num_threads=100)
    solver_results_3.append(solution_3)
    solver_results_4.append(solution_4)

flattened_solver_results_3 = [solver_result for sublist in solver_results_3 for solver_result in sublist]
flattened_solver_results_4 = [solver_result for sublist in solver_results_4 for solver_result in sublist]
SolverResult.to_json(flattened_solver_results_3, 'logs/multiplication/mult_memorize_solver_results_3.jsonl')
SolverResult.to_json(flattened_solver_results_4, 'logs/multiplication/mult_memorize_solver_results_4.jsonl')

judges = {'CONTAINS_DIGIT_JUDGE':CONTAINS_DIGIT_JUDGE}

for name, judge in judges.items():
    judge_results_3 = []
    judge_results_4 = []
    for i, solver_results in enumerate(solver_results_3):
        print(f'Judging gpt-3 responses with {i+1} digits')
        judge_results_3.append(judge.judge_solver_results(solver_results, num_threads=100))
    for i, solver_results in enumerate(solver_results_4):
        print(f'Judging gpt-4 responses with {i+1} digits')
        judge_results_4.append(judge.judge_solver_results(solver_results, num_threads=100))

    flattened_judge_results_3 = [judge_result for sublist in judge_results_3 for judge_result in sublist]
    flattened_judge_results_4 = [judge_result for sublist in judge_results_4 for judge_result in sublist]

    JudgeResult.to_json(flattened_judge_results_3, f'logs/multiplication/mult_memorize_judge_results_3_{name}.jsonl')
    JudgeResult.to_json(flattened_judge_results_4, f'logs/multiplication/mult_memorize_judge_results_4_{name}.jsonl')