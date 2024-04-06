from src.json_serialization import (
    deserialize_solver_results_from_json,
    serialize_judge_results_to_json,
)

from ..judge import CONTAINS_DIGIT_JUDGE

solver_result_names = ["logs/multiplication/mult_memorize_solver_results"]
judges = {"CONTAINS_DIGIT_JUDGE": CONTAINS_DIGIT_JUDGE}
batch = 1000

for solver_result_name in solver_result_names:
    solver_results_3_flat = deserialize_solver_results_from_json(
        f"{solver_result_name}_3.jsonl"
    )
    solver_results_4_flat = deserialize_solver_results_from_json(
        f"{solver_result_name}_4.jsonl"
    )

    assert len(solver_results_3_flat) % batch == 0
    assert len(solver_results_4_flat) % batch == 0
    solver_results_3 = [
        solver_results_3_flat[i * batch : (i + 1) * batch]
        for i in range(int(len(solver_results_3_flat) / batch))
    ]
    solver_results_4 = [
        solver_results_4_flat[i * batch : (i + 1) * batch]
        for i in range(int(len(solver_results_4_flat) / batch))
    ]

    for name, judge in judges.items():
        judge_results_3 = []
        judge_results_4 = []
        for i, solver_results in enumerate(solver_results_3):
            print(f"Judging gpt-3 responses with {i+1} digits")
            judge_results_3.append(
                judge.judge_solver_results(solver_results, num_threads=100)
            )
        for i, solver_results in enumerate(solver_results_4):
            print(f"Judging gpt-4 responses with {i+1} digits")
            judge_results_4.append(
                judge.judge_solver_results(solver_results, num_threads=100)
            )

        flattened_judge_results_3 = [
            judge_result for sublist in judge_results_3 for judge_result in sublist
        ]
        flattened_judge_results_4 = [
            judge_result for sublist in judge_results_4 for judge_result in sublist
        ]

        serialize_judge_results_to_json(
            flattened_judge_results_3,
            f"logs/multiplication/mult_memorize_judge_results_3_{name}.jsonl",
        )
        serialize_judge_results_to_json(
            flattened_judge_results_4,
            f"logs/multiplication/mult_memorize_judge_results_4_{name}.jsonl",
        )
