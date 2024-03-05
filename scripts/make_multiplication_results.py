from sample import Sample
from solver import Solver, get_gpt_3_string, get_gpt_4_string, SolverResult
from judge import CONTAINS_DIGIT_JUDGE, JudgeResult

gpt_3_string = get_gpt_3_string()
gpt_4_string = get_gpt_4_string()

samples_1 = Sample.from_json('samples/multiplication/multiplication_1000_1_42.jsonl')
samples_2 = Sample.from_json('samples/multiplication/multiplication_1000_2_42.jsonl')
samples_3 = Sample.from_json('samples/multiplication/multiplication_1000_3_42.jsonl')

solver_4 = Solver(gpt_3_string, {'temperature': 0.0, 'max_tokens': 500, 'seed': 42})
solver_3 = Solver(gpt_4_string, {'temperature': 0.0, 'max_tokens': 500, 'seed': 42})

equalsJudge = CONTAINS_DIGIT_JUDGE

solver_results_3 = []
solver_results_4 = []

for i, samples in enumerate([samples_1, samples_2 , samples_3]):
    print(f'Solving samples with {i+1} digits with gpt-3')
    solution_3 = solver_3.solve_samples(samples, num_threads=100, do_censor=False)
    print(f'Solving samples with {i+1} digits with gpt-4')
    solution_4 = solver_4.solve_samples(samples, num_threads=100, do_censor=False)
    solver_results_3.append(solution_3)
    solver_results_4.append(solution_4)

flattened_solver_results_3 = [solver_result for sublist in solver_results_3 for solver_result in sublist]
flattened_solver_results_4 = [solver_result for sublist in solver_results_4 for solver_result in sublist]
SolverResult.to_json(flattened_solver_results_3, 'logs/multiplication2/multiplication2_solver_results_3.jsonl')
SolverResult.to_json(flattened_solver_results_4, 'logs/multiplication2/multiplication2_solver_results_4.jsonl')

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

JudgeResult.to_json(flattened_judge_results_3, 'logs/multiplication2/multiplication2_judge_results_3.jsonl')
JudgeResult.to_json(flattened_judge_results_4, 'logs/multiplication2/multiplication2_judge_results_4.jsonl')