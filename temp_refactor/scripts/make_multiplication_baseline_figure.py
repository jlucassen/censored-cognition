from sample import Sample
from solver import Solver, GPT_3_STRING, GPT_4_STRING, SolverResult
from judge import EQUALS_JUDGE, JudgeResult

import matplotlib.pyplot as plt
import numpy as np

samples_1 = Sample.from_json('samples/multiplication_100_1_42_baseline.jsonl')
samples_3 = Sample.from_json('samples/multiplication_100_3_42_baseline.jsonl')
samples_2 = Sample.from_json('samples/multiplication_100_2_42_baseline.jsonl')
samples_4 = Sample.from_json('samples/multiplication_100_4_42_baseline.jsonl')
samples_5 = Sample.from_json('samples/multiplication_100_5_42_baseline.jsonl')

solver_4 = Solver(GPT_4_STRING, {'temperature': 0.0, 'max_tokens': 20, 'seed': 42})
solver_3 = Solver(GPT_3_STRING, {'temperature': 0.0, 'max_tokens': 20, 'seed': 42})

equalsJudge = EQUALS_JUDGE

solver_results_3 = []
solver_results_4 = []

for i, samples in enumerate([samples_1, samples_2, samples_3, samples_4, samples_5]):
    print(f'Solving samples with {i+1} digits with gpt-3')
    solution_3 = solver_3.solve_samples(samples, num_threads=10)
    print(f'Solving samples with {i+1} digits with gpt-4')
    solution_4 = solver_4.solve_samples(samples, num_threads=10)
    solver_results_3.append(solution_3)
    solver_results_4.append(solution_4)

flattened_solver_results_3 = [solver_result for sublist in solver_results_3 for solver_result in sublist]
flattened_solver_results_4 = [solver_result for sublist in solver_results_4 for solver_result in sublist]
SolverResult.to_json(flattened_solver_results_3, 'logs/multiplication/multiplication_baseline_solver_results_3.jsonl')
SolverResult.to_json(flattened_solver_results_4, 'logs/multiplication/multiplication_baseline_solver_results_4.jsonl')

judge_results_3 = []
judge_results_4 = []
for i, solver_results in enumerate(solver_results_3):
    print(f'Judging gpt-3 responses with {i+1} digits')
    judge_results_3.append(equalsJudge.judge_solver_results(solver_results))
for i, solver_results in enumerate(solver_results_4):
    print(f'Judging gpt-4 responses with {i+1} digits')
    judge_results_4.append(equalsJudge.judge_solver_results(solver_results))

flattened_judge_results_3 = [judge_result for sublist in judge_results_3 for judge_result in sublist]
flattened_judge_results_4 = [judge_result for sublist in judge_results_4 for judge_result in sublist]

JudgeResult.to_json(flattened_judge_results_3, 'logs/multiplication/multiplication_baseline_judge_results_3.jsonl')
JudgeResult.to_json(flattened_judge_results_4, 'logs/multiplication/multiplication_baseline_judge_results_4.jsonl')

digits = ('1', '2', '3', '4', '5')
models = {
    'gpt-3': judge_results_3,
    'gpt-4': judge_results_4,
}

x = np.arange(len(digits))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for model_bar, responses in models.items():
    metric = [sum([result.correct for result in results]) for results in responses]
    offset = width * multiplier
    rects = ax.bar(x + offset, metric, width, label=model_bar)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('# correct')
ax.set_xlabel('# digits in each multiplicand')
ax.set_title('Multiplication Memorization Baseline')
ax.set_xticks(x + width, digits)
ax.legend(loc='upper right', ncols=2)
ax.set_ylim(0, 100)

plt.savefig('figs/multiplication_memorization_baseline.png')
plt.show()