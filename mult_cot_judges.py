from judge import JudgeResult, CONTAINS_DIGIT_JUDGE
from solver import SolverResult

solver_result_names = ['logs/multiplication/mult_uncensor_solver_results']
judges = {'CONTAINS_DIGIT_JUDGE':CONTAINS_DIGIT_JUDGE}
batch = 1000

for solver_result_name in solver_result_names:
    solver_results_3_flat = SolverResult.from_json(f'{solver_result_name}_3.jsonl')
    solver_results_4_flat = SolverResult.from_json(f'{solver_result_name}_4.jsonl')

    for name, judge in judges.items():
        print(f'Judging gpt-3 responses')
        judge_results_3 = judge.judge_solver_results(solver_results_3_flat, num_threads=100)
        print(f'Judging gpt-4 responses')
        judge_results_4 = judge.judge_solver_results(solver_results_4_flat, num_threads=100)

        JudgeResult.to_json(judge_results_3, f'logs/multiplication/mult_uncensor_judge_results_3_{name}.jsonl')
        JudgeResult.to_json(judge_results_4, f'logs/multiplication/mult_uncensor_judge_results_4_{name}.jsonl')