import fire

from run import run


def main(num_threads: int = 10, upsample: int = 3):
    solvers = [
        "tryhard/gpt-3.5-turbo",
        "tryhard/gpt-4-1106-preview",
        "tryhard-hint-1/gpt-3.5-turbo",
        "tryhard-hint-1/gpt-4-1106-preview",
    ]

    eval_path = "data/prod_5_ints_1to20.jsonl"

    for solver in solvers:
        run(solver, eval_path, num_threads=num_threads, upsample=upsample)


if __name__ == "__main__":
    fire.Fire(main)
