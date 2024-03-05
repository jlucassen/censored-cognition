import fire
import yaml

from eval import CensoredCognition
from solver import Solver

PATH_TO_SOLVERS = "solvers.yaml"


def get_solvers() -> dict:
    with open(PATH_TO_SOLVERS, "r") as f:
        solvers = yaml.safe_load(f)

    return solvers


def run(solver_name: str, path_to_task: str, num_threads: int = 4, upsample: int = 10, **kwargs):
    """
    Run a solver on a task.

    Args:
        solver_name: The name of the solver to run. Solvers are defined in solvers.yaml.
        path_to_task: The path to the task to run the solver on.
        kwargs: Additional arguments to pass to the solver.
    """
    solvers = get_solvers()
    solver_args = solvers[solver_name]
    solver_args["name"] = solver_name
    solver = Solver(**solver_args)
    eval = CensoredCognition(path_to_task, upsample=upsample)
    eval.run(solver, num_threads=num_threads)


if __name__ == "__main__":
    fire.Fire(run)
