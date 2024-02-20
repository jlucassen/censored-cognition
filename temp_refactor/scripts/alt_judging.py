import matplotlib.pyplot as plt
import numpy as np

from solver import SolverResult
from judge import EQUALS_JUDGE, CONTAINS_JUDGE, EQUALS_DIGIT_JUDGE, CONTAINS_DIGIT_JUDGE

def make_plot(judge_results_3, judge_results_4, title_addendum, savefilename):
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
    ax.set_title(f'Multiplication Memorization Baseline, {title_addendum}')
    ax.set_xticks(x + width, digits)
    ax.legend(loc='upper right', ncols=2)
    ax.set_ylim(0, 100)

    plt.savefig(f'figs/{savefilename}.png')
    plt.show()

solver_results_3 = SolverResult.from_json('logs/multiplication/multiplication_baseline_solver_results_3.jsonl')
solver_results_4 = SolverResult.from_json('logs/multiplication/multiplication_baseline_solver_results_4.jsonl')

for name, judge in {'EQUALS_JUDGE':EQUALS_JUDGE,'CONTAINS_JUDGE':CONTAINS_JUDGE, 'EQUALS_DIGIT_JUDGE':EQUALS_DIGIT_JUDGE, 'CONTAINS_DIGIT_JUDGE':CONTAINS_DIGIT_JUDGE}.items():
    judge_results_3_flat = judge.judge_solver_results(solver_results_3)
    judge_results_4_flat = judge.judge_solver_results(solver_results_4)
    # divide up flattened judge results into lists of 100
    assert len(judge_results_3_flat)%100 == 0
    assert len(judge_results_4_flat)%100 == 0
    judge_results_3 = [judge_results_3_flat[i*100:(i+1)*100] for i in range(int(len(judge_results_3_flat)/100))]
    judge_results_4 = [judge_results_4_flat[i*100:(i+1)*100] for i in range(int(len(judge_results_4_flat)/100))]
    make_plot(judge_results_3, judge_results_4, title_addendum=name, savefilename=f'multiplication_memorization_baseline_{name}')