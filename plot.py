import matplotlib.pyplot as plt

from utils import load_jsonl

log_files = [
    "logs/log_2024-01-14_16-18-05.jsonl",
    "logs/log_2024-01-14_16-20-49.jsonl",
    "logs/log_2024-01-14_16-26-31.jsonl",
    "logs/log_2024-01-14_16-29-45.jsonl",
]


def extract_run_info(log_file):
    lines = load_jsonl(log_file)
    run_spec = lines[0]
    metrics = lines[-1]
    assert metrics["type"] == "metrics"
    return run_spec, metrics


def plot(log_files):
    fig, ax = plt.subplots(figsize=(12, 6))  # Increase the width of the plot

    results = []

    for log_file in log_files:
        run_spec, metrics = extract_run_info(log_file)
        solver = run_spec["solver"]
        correct_percent = metrics["correct_percent"]
        results.append((solver, correct_percent))

    ax.bar(*zip(*results))
    plt.savefig("results.png")
    plt.show()


if __name__ == "__main__":
    plot(log_files)
