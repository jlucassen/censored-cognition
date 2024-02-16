# %%
from sample import Sample
from solver import Solver
from judge import EqualsJudge

import matplotlib.pyplot as plt
import numpy as np

# %%

samples_1 = Sample.from_json('samples/multiplication_100_1_42_baseline.jsonl')
samples_2 = Sample.from_json('samples/multiplication_100_2_42_baseline.jsonl')
samples_3 = Sample.from_json('samples/multiplication_100_3_42_baseline.jsonl')
samples_4 = Sample.from_json('samples/multiplication_100_4_42_baseline.jsonl')
samples_5 = Sample.from_json('samples/multiplication_100_5_42_baseline.jsonl')

solver_4 = Solver('gpt-4-0125-preview')
solver_3 = Solver('gpt-3.5-turbo-0125')

equalsJudge = EqualsJudge()

results_3 = []
results_4 = []

# %%
for i, samples in enumerate([samples_1, samples_2, samples_3, samples_4, samples_5]):
    print(f'Solving samples with {i+1} digits with gpt-3')
    solution_3 = solver_3.solve_samples(samples, equalsJudge, max_tokens=10, num_threads=10)
    #print(f'Solving samples with {i+1} digits with gpt-4')
    #solution_4 = solver_4.solve_samples(samples, equalsJudge, max_tokens=10, num_threads=1)
    results_3.append(solution_3)
    results_4.append(solution_3)#4)


# %%
digits = ('1', '2', '3', '4', '5')
models = {
    'gpt-3': results_3,
    'gpt-4': results_4,
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

plt.savefig('multiplication_memorization_baseline.png')
plt.show()