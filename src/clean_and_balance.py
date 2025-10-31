# clean_and_balance.py
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import warnings, os, sys

warnings.filterwarnings("ignore")

INFILE = "feature_engineered_data.csv"
CLEAN_FILE = "feature_engineered_data_clean.csv"
BALANCED_FILE = "balanced_data.csv"

def try_read_csv(path):
    # try normal read
    try:
        df = pd.read_csv(path)
        # If it's one very long single column, attempt another parse below
        if df.shape[1] == 1:
            # attempt to split by comma
            s = df.iloc[:, 0].astype(str)
            # if first line has header-looking content, use it
            first = s.iloc[0]
            # split first row to detect number of columns
            parts = first.split(",")
            if len(parts) > 3:
                splitted = s.str.split(",", expand=True)
                df2 = splitted
                # try to use first row as header
                df2.columns = df2.iloc[0]
                df2 = df2.drop(index=0).reset_index(drop=True)
                return df2
        return df
    except Exception as e:
        print("CSV read failed:", e)
        sys.exit(1)

def coerce_numeric_series(s):
    # try to convert to numeric, handling commas and spaces
    s2 = s.astype(str).str.strip().replace({"": np.nan, "None": np.nan, "none": np.nan})
    # common boolean-like strings
    s2 = s2.replace({"false": "0", "False": "0", "true": "1", "True": "1", "v": "0"})
    # try numeric
    try:
        return pd.to_numeric(s2, errors="coerce")
    except:
        return s2

def make_numeric_features(df):
    df = df.copy()
    # Standard columns we expect and fallback names
    # If columns don't exist, create defaults or try to derive
    if 'session_duration' not in df.columns:
        # try to find something that looks numeric in columns
        for col in df.columns:
            if 'duration' in col.lower() or 'time' in col.lower():
                df['session_duration'] = coerce_numeric_series(df[col])
                break
    else:
        df['session_duration'] = coerce_numeric_series(df['session_duration'])

    if 'command_count' not in df.columns:
        for col in df.columns:
            if 'command' in col.lower() and 'count' in col.lower():
                df['command_count'] = coerce_numeric_series(df[col])
                break
    else:
        df['command_count'] = coerce_numeric_series(df['command_count'])

    if 'failed_logins' not in df.columns:
        for col in df.columns:
            if 'failed' in col.lower() and 'login' in col.lower():
                df['failed_logins'] = coerce_numeric_series(df[col])
                break
    else:
        df['failed_logins'] = coerce_numeric_series(df['failed_logins'])

    # derive a simple command_len numeric from `common_commands` or `command` if present
    if 'common_commands' in df.columns:
        df['common_commands'] = df['common_commands'].astype(str)
        df['common_commands_enc'] = df['common_commands'].str.len()  # simple proxy
    elif 'command' in df.columns:
        df['common_commands_enc'] = df['command'].astype(str).str.len()
    else:
        df['common_commands_enc'] = 0

    # fill NaN numeric columns with 0
    for c in ['session_duration', 'command_count', 'failed_logins', 'common_commands_enc']:
        if c not in df.columns:
            df[c] = 0
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    return df[['session_duration','command_count','failed_logins','common_commands_enc']]

def encode_label(y):
    # keep original label values but also return encoded mapping
    le = LabelEncoder()
    y_enc = le.fit_transform(y.astype(str))
    return y_enc, le

def main():
    if not os.path.exists(INFILE):
        print("Input file not found:", INFILE)
        return

    print("Reading", INFILE)
    df = try_read_csv(INFILE)
    print("Initial shape:", df.shape)
    print("Columns:", list(df.columns)[:30])

    # Try to find label column names
    label_col = None
    for cand in ('attack_type', 'attack', 'label', 'type'):
        if cand in df.columns:
            label_col = cand
            break
    if label_col is None:
        # try to detect column that contains known strings
        for col in df.columns:
            sample = df[col].astype(str).str.lower().head(20).tolist()
            if any(x in ('brute force','command injection','other','bruteforce','command') for x in sample):
                label_col = col
                break

    if label_col is None:
        print("No obvious label column found. You may need to supply a dataset with an 'attack_type' or 'label' column.")
        print("I can generate a synthetic dataset for you instead. To do that run: python3 generate_synthetic_data.py")
        return

    print("Using label column:", label_col)
    features_df = make_numeric_features(df)
    print("Feature frame shape:", features_df.shape)
    # encode labels
    y_raw = df[label_col].astype(str)
    y_enc, le = encode_label(y_raw)
    print("Original label distribution:", Counter(y_raw))

    # Prepare X,y
    X = features_df
    y = y_raw  # keep string labels for SMOTE; SMOTE accepts arrays of labels

    # Encode non-numeric features in X (we already numericified)
    # Run SMOTE safely. If some classes have < k_samples, SMOTE will fail; we detect and upsample by simple resampling in that case.
    class_counts = Counter(y)
    min_count = min(class_counts.values())
    print("Class counts:", class_counts)
    # If any class has fewer than 3 samples, don't use SMOTE; do simple upsampling via resample
    use_smote = True
    if min_count < 3:
        use_smote = False

    if use_smote:
        try:
            print("Applying SMOTE...")
            sm = SMOTE(random_state=42, k_neighbors=2)
            X_res, y_res = sm.fit_resample(X, y)
        except Exception as e:
            print("SMOTE failed:", e)
            use_smote = False

    if not use_smote:
        # simple upsample minority classes to match the max class count
        print("Using simple upsampling (SMOTE not applicable).")
        from sklearn.utils import resample
        df_full = X.copy()
        df_full['label'] = y
        max_n = max(Counter(y).values())
        frames = []
        for cls, cnt in Counter(y).items():
            part = df_full[df_full['label'] == cls]
            if cnt < max_n:
                part_up = resample(part, replace=True, n_samples=max_n, random_state=42)
                frames.append(part_up)
            else:
                frames.append(part)
        df_bal = pd.concat(frames).sample(frac=1, random_state=42).reset_index(drop=True)
        X_res = df_bal.drop(columns=['label'])
        y_res = df_bal['label']

    # Save cleaned feature file
    clean_out = df.copy()
    clean_out[['session_duration','command_count','failed_logins','common_commands_enc']] = X_res.iloc[:len(clean_out), :len(X_res.columns)].values if False else X_res.head(len(clean_out)).values[:,:4] if False else None
    # instead save explicit cleaned features + labels (safe)
    cleaned = pd.DataFrame(X_res, columns=X.columns)
    cleaned['label'] = y_res
    cleaned.to_csv(CLEAN_FILE, index=False)
    print("Saved cleaned features to", CLEAN_FILE)
    # Now balanced_data.csv: numeric columns + label
    balanced = cleaned.copy()
    balanced.to_csv(BALANCED_FILE, index=False)
    print("Saved balanced data to", BALANCED_FILE)
    print("Final balanced class distribution:", Counter(y_res))

if __name__ == "__main__":
    main()
