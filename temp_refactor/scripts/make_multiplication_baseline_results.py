from sample import Sample
from solver import Solver, GPT_3_STRING, GPT_4_STRING, SolverResult
from judge import EQUALS_DIGIT_JUDGE, JudgeResult

import matplotlib.pyplot as plt
import numpy as np

samples_1 = Sample.from_json('samples/multiplication_1000_1_42_baseline.jsonl')
samples_3 = Sample.from_json('samples/multiplication_1000_3_42_baseline.jsonl')
samples_2 = Sample.from_json('samples/multiplication_1000_2_42_baseline.jsonl')
samples_4 = Sample.from_json('samples/multiplication_1000_4_42_baseline.jsonl')
samples_5 = Sample.from_json('samples/multiplication_1000_5_42_baseline.jsonl')
samples_6 = Sample.from_json('samples/multiplication_1000_6_42_baseline.jsonl')
samples_7 = Sample.from_json('samples/multiplication_1000_7_42_baseline.jsonl')

solver_4 = Solver(GPT_4_STRING, {'temperature': 0.0, 'max_tokens': 30, 'seed': 42})
solver_3 = Solver(GPT_3_STRING, {'temperature': 0.0, 'max_tokens': 30, 'seed': 42})

equalsJudge = EQUALS_DIGIT_JUDGE

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
SolverResult.to_json(flattened_solver_results_3, 'logs/multiplication/multiplication_baseline1000_solver_results_3.jsonl')
SolverResult.to_json(flattened_solver_results_4, 'logs/multiplication/multiplication_baseline1000_solver_results_4.jsonl')

judge_results_3 = []
judge_results_4 = []
for i, solver_results in enumerate(solver_results_3):
    print(f'Judging gpt-3 responses with {i+1} digits')
    judge_results_3.append(equalsJudge.judge_solver_results(solver_results, num_threads=100))
for i, solver_results in enumerate(solver_results_4):
    print(f'Judging gpt-4 responses with {i+1} digits')
    judge_results_4.append(equalsJudge.judge_solver_results(solver_results, num_threads=100))

flattened_judge_results_3 = [judge_result for sublist in judge_results_3 for judge_result in sublist]
flattened_judge_results_4 = [judge_result for sublist in judge_results_4 for judge_result in sublist]

JudgeResult.to_json(flattened_judge_results_3, 'logs/multiplication/multiplication_baseline1000_judge_results_3.jsonl')
JudgeResult.to_json(flattened_judge_results_4, 'logs/multiplication/multiplication_baseline1000_judge_results_4.jsonl')