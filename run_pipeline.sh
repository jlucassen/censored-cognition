#!/usr/bin/env bash
# Runs the whole pipeline for the project. This will make calls to OpenAI, store some files on your system, and generate plots


poetry run python -m src.scripts.mult_cot_samples
poetry run python -m src.scripts.mult_cot_solvers
poetry run python -m src.scripts.mult_cot_judges
poetry run python -m src.scripts.mult_cot_figs
