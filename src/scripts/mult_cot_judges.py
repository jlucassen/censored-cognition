import glob

from src.json_serialization import (
    deserialize_solver_results_from_json,
    serialize_judge_results_to_json,
)

from ..judge import CONTAINS_DIGIT_JUDGE


def get_modes_to_solver_result_file_paths():
    stems = set()
    all_files_in_dir = glob.glob(
        "logs/multiplication/mult_uncensor*_solver_results_*.jsonl"
    )
    for filename in all_files_in_dir:
        # Remove _3.jsonl/_4.jsonl and solver_results
        stem = (filename[:-8]).removeprefix("logs/multiplication/")
        stem = stem.removesuffix("_solver_results")
        stems.add(stem)
    return {
        # Bit clowny: Remove logs/multiplication as a prefix and solver_results suffix and readd, but this way mode is easily readable
        stem: f"logs/multiplication/{stem}_solver_results"
        for stem in stems
    }


modes_to_solver_result_file_paths = get_modes_to_solver_result_file_paths()
judges = {"CONTAINS_DIGIT_JUDGE": CONTAINS_DIGIT_JUDGE}
batch = 1000

for mode, solver_result_file_path in modes_to_solver_result_file_paths.items():
    solver_results_3_file_path = f"{solver_result_file_path}_3.jsonl"
    solver_results_4_file_path = f"{solver_result_file_path}_4.jsonl"
    print(
        f"Running judges in mode {mode} on the files {solver_results_3_file_path} and {solver_results_4_file_path}"
    )
    solver_results_3_flat = deserialize_solver_results_from_json(
        solver_results_3_file_path
    )
    solver_results_4_flat = deserialize_solver_results_from_json(
        solver_results_4_file_path
    )

    for name, judge in judges.items():
        judge_results_3 = judge.judge_solver_results(
            solver_results_3_flat, num_threads=100
        )
        judge_results_4 = judge.judge_solver_results(
            solver_results_4_flat, num_threads=100
        )

        judge_results_3_file_path = (
            f"logs/multiplication/{mode}_judge_results_3_{name}.jsonl"
        )
        judge_results_4_file_path = (
            f"logs/multiplication/{mode}_judge_results_4_{name}.jsonl"
        )
        print(
            f"Storing judge results to {judge_results_3_file_path} and {judge_results_4_file_path}"
        )
        serialize_judge_results_to_json(judge_results_3, judge_results_3_file_path)
        serialize_judge_results_to_json(judge_results_4, judge_results_4_file_path)
