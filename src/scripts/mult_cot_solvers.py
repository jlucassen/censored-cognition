import glob

from src.json_serialization import serialize_solver_results_to_json

from ..sample import Sample
from ..solver import Solver, get_gpt_3_string, get_gpt_4_string

gpt_3_string = get_gpt_3_string()
gpt_4_string = get_gpt_4_string()


def get_modes_to_samples():
    stems = set()
    all_files_in_dir = glob.glob("samples/multiplication/mult_uncensor_*.jsonl")
    for file in all_files_in_dir:
        stem = (file.split("_1000_")[0]).removeprefix("samples/multiplication/")
        stems.add(stem)
    return {
        stem: list(
            filter(
                lambda f: f.startswith(f"samples/multiplication/{stem}_1000_"),
                all_files_in_dir,
            )
        )
        for stem in stems
    }


for mode, sample_files in get_modes_to_samples().items():
    solver_3 = Solver(gpt_3_string, {"temperature": 0.0, "max_tokens": 500, "seed": 42})
    solver_4 = Solver(gpt_4_string, {"temperature": 0.0, "max_tokens": 500, "seed": 42})

    solver_results_3 = []
    solver_results_4 = []

    print(f"Running solvers on the sample files {sample_files} in mode {mode}")
    for i, samples in enumerate(map(lambda s_f: Sample.from_json(s_f), sample_files)):
        print(f"Solving samples with {i+1} digits with gpt-3")
        solution_3 = solver_3.solve_samples(samples, num_threads=100, do_censor=False)
        print(f"Solving samples with {i+1} digits with gpt-4")
        solution_4 = solver_4.solve_samples(samples, num_threads=100, do_censor=False)
        solver_results_3.append(solution_3)
        solver_results_4.append(solution_4)

    flattened_solver_results_3 = [
        solver_result for sublist in solver_results_3 for solver_result in sublist
    ]
    flattened_solver_results_4 = [
        solver_result for sublist in solver_results_4 for solver_result in sublist
    ]
    solver_results_3_file = f"logs/multiplication/{mode}_solver_results_3.jsonl"
    print(f"Storing solver results in {solver_results_3_file}")
    serialize_solver_results_to_json(
        flattened_solver_results_3,
        solver_results_3_file,
    )
    solver_results_4_file = f"logs/multiplication/{mode}_solver_results_4.jsonl"
    print(f"Storing solver results in {solver_results_4_file}")
    serialize_solver_results_to_json(
        flattened_solver_results_4,
        solver_results_4_file,
    )
