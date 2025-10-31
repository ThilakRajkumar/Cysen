# generate_attack_logs.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

N = 2000
rng = np.random.RandomState(42)

base = datetime.utcnow()

def rand_time(i):
    return (base + timedelta(seconds=int(i*30) + rng.randint(0,60))).isoformat() + "+00:00"

def rand_ip():
    return f"171.79.{rng.randint(0,255)}.{rng.randint(1,254)}"

def rand_username():
    return rng.choice(["root","admin","user","test","guest","oracle","ftp"])

def rand_password():
    return rng.choice(["", "1234", "root", "pass", "toor", "2233", "3344", "password"])

commands = ["ls","cat password.txt","mkdir phoenix","touch password.txt","cd /tmp","echo 'hi'","exit","ifconfig","uname -a"]
common_cmd_tags = ["ls","other","echo","cat","mkdir","touch","ifconfig","exit"]

rows = []
for i in range(N):
    ts = rand_time(i)
    ip = rand_ip()
    user = rand_username() if rng.rand() < 0.6 else ""
    pwd = rand_password() if user else ""
    cmd = rng.choice(commands) if rng.rand() < 0.6 else ""
    session = f"{rng.randint(1,999999):x}{rng.randint(1,999999):x}"
    eventid = f"{rng.randint(100000,999999):x}"
    # Create labels with imbalance
    r = rng.rand()
    if r < 0.6:
        attack = "Command Injection"
        session_duration = rng.randint(30,400)
        command_count = rng.randint(5,30)
        failed_logins = rng.randint(0,2)
        common_cmd = rng.choice(common_cmd_tags)
    elif r < 0.9:
        attack = "Brute Force"
        session_duration = rng.randint(5,120)
        command_count = rng.randint(0,5)
        failed_logins = rng.randint(1,10)
        common_cmd = "other"
    else:
        attack = "Other"
        session_duration = rng.randint(1,200)
        command_count = rng.randint(0,10)
        failed_logins = rng.randint(0,3)
        common_cmd = "other"

    rows.append([
        ts, ip, user, pwd, cmd, session, eventid, attack,
        session_duration, float(command_count), float(failed_logins), common_cmd
    ])

df = pd.DataFrame(rows, columns=[
    "timestamp","src_ip","username","password","command","session","eventid","attack_type",
    "session_duration","command_count","failed_logins","common_commands"
])

df.to_csv("feature_engineered_data.csv", index=False)
# create X_test (20% holdout without labels)
X = df[['session_duration','command_count','failed_logins','common_commands']].copy()
X_test = X.sample(frac=0.2, random_state=42).reset_index(drop=True)
# encode simple common_commands length to match pipeline
X_test['common_commands'] = X_test['common_commands'].astype(str)
X_test.to_csv("X_test.csv", index=False)
print("Wrote feature_engineered_data.csv (N=", len(df), ") and X_test.csv")
