# Usage

0. Put an OpenAI key for the project in the environment variables

```bash
export OPENAI_API_KEY=sk-...
```

1. First install the venv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create necessary directories

```
mkdir -p logs/all_runs/judge_results
mkdir -p logs/multiplication
mkdir -p logs/all_runs/solver_results
mkdir -p samples/multiplication
```

3. Then you can run the scripts

```bash
python -m src.scripts.mult_memorize_samples
python -m src.scripts.mult_memorize_solvers
python -m src.scripts.mult_memorize_judges
python -m src.scripts.mult_memorize_figs
```
