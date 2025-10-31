#!/usr/bin/env bash
set -euo pipefail
echo "Activate your venv before running or ensure python3 is available."
echo "Running demo pipeline (synthetic data)..."
# assume src/*.py exist and requirements installed
python3 src/generate_attack_logs.py
python3 src/clean_and_balance.py
python3 src/train_model_1.py
python3 src/test_geo.py
echo "Demo finished. See predictions_with_geo.csv"
