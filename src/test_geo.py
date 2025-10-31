#!/usr/bin/env python3
"""
test_geo.py
- Loads attack_classifier_model.pkl and label encoder (if present)
- Loads X_test.csv (or falls back to last row of feature_engineered_data.csv)
- Prepares features, predicts, optionally enriches with IPInfo (from .env)
- Writes predictions_with_geo.csv
"""
import os
import joblib
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()

MODEL_FILE = "attack_classifier_model.pkl"
LABEL_ENCODER_FILE = "label_encoder.pkl"
X_TEST = "X_test.csv"
OUT_PRED = "predictions_with_geo.csv"
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN", "")

# small mapping for demo; adjust as needed
COMMON_CMD_MAP = {
    'ls':1, 'cd':2, 'mkdir':3, 'cat':4, 'echo':5, 'rm':6, 'cp':7, 'wget':8, 'other':9, 'touch':10, 'exit':11
}

def get_geo_ipinfo(ip, token, timeout=6):
    if not token or not ip:
        return None
    try:
        r = requests.get(f"https://ipinfo.io/{ip}?token={token}", timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return joblib.load(path)

def prepare_test_features(df):
    df = df.copy()
    if 'common_commands' in df.columns:
        df['common_commands_enc'] = df['common_commands'].map(COMMON_CMD_MAP).fillna(0).astype(float)
        df = df.drop(columns=['common_commands'])
    # drop label columns if exist
    for c in ('label','attack_type'):
        if c in df.columns:
            df = df.drop(columns=[c])
    # coerce non-numeric columns where possible
    for col in df.columns:
        if df[col].dtype == object and col != 'src_ip':
            df[col] = pd.to_numeric(df[col].astype(str).str.strip().replace({'': None}), errors='coerce')
            if df[col].isna().all():
                df[col] = df[col].astype(str).str.len().fillna(0)
    return df

def align_features_to_model(X, model):
    try:
        expected = list(model.feature_names_in_)
    except Exception:
        expected = None
    if expected:
        for c in expected:
            if c not in X.columns:
                X[c] = 0
        X = X[expected]
    return X

def ensure_X_test_has_ip():
    # if X_test.csv missing or missing src_ip, attempt to create it from last row of feature_engineered_data.csv
    if os.path.exists(X_TEST):
        df = pd.read_csv(X_TEST)
        if 'src_ip' in df.columns and df['src_ip'].notna().any():
            return df
    # fallback: build X_test from last row of feature_engineered_data.csv if present
    feat = "feature_engineered_data.csv"
    if os.path.exists(feat):
        fdf = pd.read_csv(feat)
        if len(fdf) > 0:
            cols = []
            for c in ['session_duration','command_count','failed_logins','common_commands','src_ip']:
                if c in fdf.columns:
                    cols.append(c)
            row = fdf.tail(1)[cols].copy()
            if 'src_ip' not in row.columns:
                row['src_ip'] = ''
            row.to_csv(X_TEST, index=False)
            return row
    raise FileNotFoundError("No X_test.csv and no feature_engineered_data.csv fallback available.")

def main():
    print("Loading model:", MODEL_FILE)
    model = load_model(MODEL_FILE)

    label_encoder = None
    if os.path.exists(LABEL_ENCODER_FILE):
        try:
            label_encoder = joblib.load(LABEL_ENCODER_FILE)
            print("Loaded label encoder.")
        except Exception:
            label_encoder = None

    print("Preparing X_test...")
    X_raw = ensure_X_test_has_ip()
    ip_col = None
    for cand in ("src_ip","ip","source_ip"):
        if cand in X_raw.columns:
            ip_col = cand
            break

    X_pre = prepare_test_features(X_raw)
    X_aligned = align_features_to_model(X_pre, model)

    print("Predicting...")
    preds = model.predict(X_aligned)
    out = X_raw.copy()
    out['pred_label_enc'] = preds
    if label_encoder is not None:
        try:
            out['pred_label'] = label_encoder.inverse_transform(preds.astype(int))
        except Exception:
            out['pred_label'] = preds
    else:
        out['pred_label'] = preds

    if hasattr(model, "predict_proba"):
        try:
            out["pred_proba_max"] = model.predict_proba(X_aligned).max(axis=1)
        except Exception:
            out["pred_proba_max"] = None
    else:
        out["pred_proba_max"] = None

    # geo enrichment if IP column present
    if ip_col and IPINFO_TOKEN:
        print("Performing geo enrichment for IPs in column:", ip_col)
        geo_list = []
        for ip in out[ip_col].fillna("").astype(str):
            if not ip:
                geo_list.append(None)
                continue
            geo_list.append(get_geo_ipinfo(ip, IPINFO_TOKEN))
        out["geo_raw"] = geo_list
        out["geo_country"] = out["geo_raw"].apply(lambda x: x.get("country") if isinstance(x, dict) else None)
        out["geo_city"] = out["geo_raw"].apply(lambda x: x.get("city") if isinstance(x, dict) else None)
    else:
        if not IPINFO_TOKEN:
            print("IPINFO_TOKEN not set — skipping geo enrichment.")
        elif not ip_col:
            print("No IP column found in X_test.csv — skipping geo enrichment.")
        out["geo_raw"] = None
        out["geo_country"] = None
        out["geo_city"] = None

    out.to_csv(OUT_PRED, index=False)
    print(f"Saved predictions to {OUT_PRED}. Rows: {len(out)}")

if __name__ == "__main__":
    main()
