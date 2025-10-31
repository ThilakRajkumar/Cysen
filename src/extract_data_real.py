import json
import pandas as pd

# Load Cowrie log JSON
with open("var/log/cowrie/cowrie.json", "r") as f:
    lines = f.readlines()

data = []
for line in lines:
    try:
        log = json.loads(line)
        if log.get("eventid") in ["cowrie.login.failed", "cowrie.session.connect", "cowrie.session.closed"]:
            entry = {
                "timestamp": log.get("timestamp"),
                "src_ip": log.get("src_ip"),
                "username": log.get("username"),
                "password": log.get("password"),
                "duration": log.get("duration"),
                "eventid": log.get("eventid"),
                "message": log.get("message")
            }
            data.append(entry)
    except json.JSONDecodeError:
        continue

# Convert to DataFrame
df = pd.DataFrame(data)
df.to_csv("real_attack_data.csv", index=False)
print(f"✅ Extracted {len(df)} log entries into real_attack_data.csv")
print(df.head())
