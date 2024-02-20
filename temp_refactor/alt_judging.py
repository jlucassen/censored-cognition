from result import SolverResult
from judge import EQUALS_JUDGE, CONTAINS_JUDGE, EQUALS_DIGIT_JUDGE, CONTAINS_DIGIT_JUDGE

solver_results_3 = SolverResult.from_json('logs/multiplication/multiplication_baseline_solver_results_3.jsonl')
solver_results_4 = SolverResult.from_json('logs/multiplication/multiplication_baseline_solver_results_4.jsonl')

print(solver_results_3[0].sample)

for judge in [EQUALS_JUDGE, CONTAINS_JUDGE, EQUALS_DIGIT_JUDGE, CONTAINS_DIGIT_JUDGE]:
    for results in [solver_results_3, solver_results_4]:
        judge_results = judge.judge_solver_results(results)
        accuracy = sum([judge_result.judge_bool for judge_result in judge_results])
        print(f"{accuracy=}, {judge.judge_function.__name__=}, {results[0].solver.model=}")