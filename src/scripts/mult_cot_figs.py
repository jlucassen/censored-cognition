import glob

import matplotlib.pyplot as plt
import numpy as np
from src.json_serialization import deserialize_judge_results_from_json


def make_plot(judge_results_3, judge_results_4, title_addendum, savefilename):
    digits = tuple([str(x) for x in range(1, len(judge_results_3) + 1)])
    models = {
        "gpt-3": judge_results_3,
        "gpt-4": judge_results_4,
    }

    x = np.arange(len(digits))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for model_bar, responses in models.items():
        metric = [
            sum([result.correct == "True" for result in results]) / len(results)
            for results in responses
        ]
        offset = width * multiplier
        ax.bar(x + offset, metric, width, label=model_bar)
        stds = np.sqrt(np.multiply(metric, [1 - m for m in metric])) / np.sqrt(
            len(responses[0]) - 1
        )
        ax.errorbar(
            x + offset, metric, yerr=stds * 1.96, color="k", fmt="none", capsize=3
        )  # 95% confidence interval
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("fraction correct")
    ax.set_xlabel("number of digits in each multiplicand")
    ax.set_title(f"Multiplication Memorization Baseline, {title_addendum}")
    ax.set_xticks(x + width, digits)
    ax.legend(loc="upper right", ncols=2)
    ax.set_ylim(0, 1)

    plot_filename = f"figs/multiplication/{savefilename}.png"
    print(f"Saving file under {plot_filename}")
    plt.savefig(plot_filename)
    # plt.show()


def get_modes_to_judge_result_file_path():
    stems = set()
    all_files_in_dir = glob.glob("logs/multiplication/*_judge_results_3*.jsonl")
    for file in all_files_in_dir:
        stems.add(
            (file.split("_judge_results_")[0]).removeprefix("logs/multiplication/")
        )
    return {stem: f"logs/multiplication/{stem}" for stem in stems}


batch = 1000
modes_to_judge_result_file_path = get_modes_to_judge_result_file_path()
judges = ["CONTAINS_DIGIT_JUDGE"]

for mode, judge_results_file_path in modes_to_judge_result_file_path.items():
    print(f"Loading judge results for mode {mode}")
    for judge in judges:
        judge_results_3_file_path = (
            f"{judge_results_file_path}_judge_results_3_{judge}.jsonl"
        )
        judge_results_4_file_path = (
            f"{judge_results_file_path}_judge_results_4_{judge}.jsonl"
        )
        print(
            f"Loading judge results from {judge_results_3_file_path} and {judge_results_4_file_path}"
        )
        judge_results_3_flat = deserialize_judge_results_from_json(
            judge_results_3_file_path
        )
        judge_results_4_flat = deserialize_judge_results_from_json(
            judge_results_4_file_path
        )

        # divide up flattened judge results into lists of 1000
        assert len(judge_results_3_flat) % batch == 0
        assert len(judge_results_4_flat) % batch == 0
        judge_results_3 = [
            judge_results_3_flat[i * batch : (i + 1) * batch]
            for i in range(int(len(judge_results_3_flat) / batch))
        ]
        judge_results_4 = [
            judge_results_4_flat[i * batch : (i + 1) * batch]
            for i in range(int(len(judge_results_4_flat) / batch))
        ]

        make_plot(
            judge_results_3,
            judge_results_4,
            title_addendum=judge,
            savefilename=f"{mode}_{judge}",
        )

print(
    f"Created {len(modes_to_judge_result_file_path) * len(judges)} plots for the following modes: {list(modes_to_judge_result_file_path.keys())} and juges: {judges}"
)
print("You can find the generated plots under figs/multiplication/*.png")
