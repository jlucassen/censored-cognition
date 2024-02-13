# %%
from sample import Sample
from solver import Solver
from judge import ContainsJudge

import matplotlib.pyplot as plt
import numpy as np

# %%

samples_1 = Sample.from_json('samples/multiplication_100_1_42_no_steps.jsonl')
samples_2 = Sample.from_json('samples/multiplication_100_2_42_no_steps.jsonl')
samples_3 = Sample.from_json('samples/multiplication_100_3_42_no_steps.jsonl')
samples_4 = Sample.from_json('samples/multiplication_100_4_42_no_steps.jsonl')
samples_5 = Sample.from_json('samples/multiplication_100_5_42_no_steps.jsonl')

solver_4 = Solver('gpt-4')
solver_3 = Solver('gpt-3.5-turbo-0125')

containsJudge = ContainsJudge()

results_3 = []
results_4 = []

# %%

for i, samples in enumerate([samples_1, samples_2, samples_3, samples_4, samples_5]):
    solution_3 = solver_3.solve_samples(samples, containsJudge)
    solution_4 = solver_4.solve_samples(samples, containsJudge)
    results_3.append(solution_3)
    results_4.append(solution_4)


# %%
species = ('1', '2', '3', '4', '5')
penguin_means = {
    'gpt-3': results_3,
    'gpt-4': results_4,
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Length (mm)')
ax.set_title('Penguin attributes by species')
ax.set_xticks(x + width, species)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 250)

plt.show()
# %%
