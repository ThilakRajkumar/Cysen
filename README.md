# Cowrie Honeypot — ML Analysis & Geo Enrichment

This repo contains scripts to process Cowrie honeypot logs, build features, train a simple classifier, and optionally enrich predictions with IP geolocation.

See `src/` for scripts:
- extract_data_real.py
- build_features_from_real.py
- clean_and_balance.py
- train_model_1.py
- test_geo.py
- generate_attack_logs.py (synthetic demo)

For a quick demo see `run_demo.sh` and `demo/sample_X_test.csv`.

**Do NOT commit** `.env` or `var/log/cowrie` or other sensitive logs.
