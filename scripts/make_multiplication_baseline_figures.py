import matplotlib.pyplot as plt
import numpy as np

from solver import SolverResult
from judge import EQUALS_JUDGE, CONTAINS_JUDGE, EQUALS_DIGIT_JUDGE, CONTAINS_DIGIT_JUDGE

def make_plot(judge_results_3, judge_results_4, title_addendum, savefilename):
    digits = tuple([str(x) for x in range(1, len(judge_results_3)+1)])
    models = {
        'gpt-3': judge_results_3,
        'gpt-4': judge_results_4,
    }

    x = np.arange(len(digits))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for model_bar, responses in models.items():
        metric = [sum([result.correct for result in results])/len(results) for results in responses]
        offset = width * multiplier
        ax.bar(x + offset, metric, width, label=model_bar)
        stds = np.sqrt(np.multiply(metric, [1-m for m in metric]))/np.sqrt(len(responses[0])-1)
        ax.errorbar(x+offset, metric, yerr = stds*1.96, color='k', fmt='none', capsize=3) # 95% confidence interval
        # ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction correct')
    ax.set_xlabel('number of digits in each multiplicand')
    ax.set_title(f'Multiplication Memorization Baseline, {title_addendum}')
    ax.set_xticks(x + width, digits)
    ax.legend(loc='upper right', ncols=2)
    ax.set_ylim(0, 1)

    plt.savefig(f'figs/multiplication_baseline/{savefilename}.png')
    plt.show()

solver_results_3 = SolverResult.from_json('logs/multiplication_baseline/multiplication_baseline1000_solver_results_3.jsonl')
solver_results_4 = SolverResult.from_json('logs/multiplication_baseline/multiplication_baseline1000_solver_results_4.jsonl')

batch = 1000

judges = {'EQUALS_JUDGE':EQUALS_JUDGE,
          'CONTAINS_JUDGE':CONTAINS_JUDGE,
          'EQUALS_DIGIT_JUDGE':EQUALS_DIGIT_JUDGE,
          'CONTAINS_DIGIT_JUDGE':CONTAINS_DIGIT_JUDGE}

for name, judge in judges.items():
    judge_results_3_flat = judge.judge_solver_results(solver_results_3, num_threads=100)
    judge_results_4_flat = judge.judge_solver_results(solver_results_4, num_threads=100)
    # divide up flattened judge results into lists of 1000
    assert len(judge_results_3_flat)%batch == 0
    assert len(judge_results_4_flat)%batch == 0
    print(len(judge_results_3_flat), len(judge_results_4_flat))
    judge_results_3 = [judge_results_3_flat[i*batch:(i+1)*batch] for i in range(int(len(judge_results_3_flat)/batch))]
    judge_results_4 = [judge_results_4_flat[i*batch:(i+1)*batch] for i in range(int(len(judge_results_4_flat)/batch))]
    make_plot(judge_results_3, judge_results_4, title_addendum=name, savefilename=f'multiplication_memorization_baseline_{name}')