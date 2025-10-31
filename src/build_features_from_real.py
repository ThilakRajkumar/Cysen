# build_features_from_real.py
"""
Aggregate real Cowrie log extracts (real_attack_data.csv) into feature rows
and append to feature_engineered_data.csv (or create it if absent).

This script aggregates by session and produces:
- session_duration (seconds)
- command_count (number of command-like events / login attempts)
- failed_logins (count of cowrie.login.failed for the session)
- common_commands (most common tokenized command or 'other')
- src_ip (source IP)
- attack_type (we'll label real data as 'Other' or 'Brute Force' heuristically)
"""

import pandas as pd
from collections import Counter
import os

IN = "real_attack_data.csv"
OUT = "feature_engineered_data.csv"

if not os.path.exists(IN):
    raise SystemExit(f"{IN} not found. Run extract_data_real.py first.")

df = pd.read_csv(IN)

# If there is no session column, try to use src_ip + timestamp grouping
# We will group by src_ip for simplicity (small logs). If session present, prefer it.
group_col = "src_ip"
if "session" in df.columns:
    group_col = "session"

rows = []
for key, g in df.groupby(group_col):
    src_ip = g['src_ip'].iloc[0] if 'src_ip' in g.columns else ''
    # duration: use max(duration) or compute from timestamps if present
    if g['duration'].notna().any():
        dur = pd.to_numeric(g['duration'], errors='coerce').dropna()
        session_duration = float(dur.max()) if len(dur)>0 else 0.0
    else:
        # fallback: set session_duration to 0 (or compute timestamps if desired)
        session_duration = 0.0

    # count events that look like commands or login attempts
    command_count = g['eventid'].str.contains('command|input|login', na=False).sum()
    # failed_logins
    failed_logins = (g['eventid'] == 'cowrie.login.failed').sum()

    # derive common_commands: find most frequent word in 'message' or 'password' or 'command'
    tokens = []
    if 'command' in g.columns:
        tokens += list(g['command'].dropna().astype(str))
    if 'message' in g.columns:
        tokens += list(g['message'].dropna().astype(str))
    if 'password' in g.columns:
        tokens += list(g['password'].dropna().astype(str))
    # pick a short proxy: most common token word
    words = []
    for t in tokens:
        for w in str(t).split():
            w = w.strip().lower()
            if len(w) > 0 and len(w) < 40:
                words.append(w)
    common = Counter(words).most_common(1)
    common_commands = common[0][0] if common else "other"

    # Heuristic attack_type labeling:
    # If failed_logins > 1 and command_count small -> Brute Force
    # If command_count large -> Command Injection
    if failed_logins >= 2 and command_count <= 3:
        attack_type = "Brute Force"
    elif command_count >= 3:
        attack_type = "Command Injection"
    else:
        attack_type = "Other"

    rows.append({
        "timestamp": g['timestamp'].iloc[0] if 'timestamp' in g.columns else "",
        "src_ip": src_ip,
        "session_duration": session_duration,
        "command_count": float(command_count),
        "failed_logins": float(failed_logins),
        "common_commands": common_commands,
        "attack_type": attack_type
    })

# build df
new_df = pd.DataFrame(rows)

# Append to existing feature_engineered_data.csv OR create new
if os.path.exists(OUT):
    existing = pd.read_csv(OUT)
    combined = pd.concat([existing, new_df], ignore_index=True)
else:
    combined = new_df

combined.to_csv(OUT, index=False)
print(f"Appended {len(new_df)} session rows to {OUT} (now {len(combined)} rows total).")
print(new_df)
