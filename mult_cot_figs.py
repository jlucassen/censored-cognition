import matplotlib.pyplot as plt
import numpy as np

from judge import JudgeResult

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
        metric = [sum([result.correct=="True" for result in results])/len(results) for results in responses]
        offset = width * multiplier
        ax.bar(x + offset, metric, width, label=model_bar)
        stds = np.sqrt(np.multiply(metric, [1-m for m in metric]))/np.sqrt(len(responses[0])-1)
        ax.errorbar(x+offset, metric, yerr = stds*1.96, color='k', fmt='none', capsize=3) # 95% confidence interval
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction correct')
    ax.set_xlabel('number of digits in each multiplicand')
    ax.set_title(f'Multiplication Memorization Baseline, {title_addendum}')
    ax.set_xticks(x + width, digits)
    ax.legend(loc='upper right', ncols=2)
    ax.set_ylim(0, 1)

    plt.savefig(f'figs/multiplication/{savefilename}.png')
    plt.show()

batch = 1000
judges = ['CONTAINS_DIGIT_JUDGE']

for name in judges:
    judge_results_3_flat = JudgeResult.from_json(f'logs/multiplication/mult_uncensor_judge_results_3_{name}.jsonl')
    judge_results_4_flat = JudgeResult.from_json(f'logs/multiplication/mult_uncensor_judge_results_4_{name}.jsonl')

    # divide up flattened judge results into lists of 1000
    assert len(judge_results_3_flat)%batch == 0
    assert len(judge_results_4_flat)%batch == 0
    judge_results_3 = [judge_results_3_flat[i*batch:(i+1)*batch] for i in range(int(len(judge_results_3_flat)/batch))]
    judge_results_4 = [judge_results_4_flat[i*batch:(i+1)*batch] for i in range(int(len(judge_results_4_flat)/batch))]

    make_plot(judge_results_3, judge_results_4, title_addendum=name, savefilename=f'mult_uncensor_{name}')