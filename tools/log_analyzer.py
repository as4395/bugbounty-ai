# Purpose:
#   Analyze and summarize findings from zero-day fuzzing stored in logs/zero_day_anomalies.json.
#   Provides a terminal report of anomaly types, payloads, and scan timestamps.

# Requirements:
#   pip install pandas

# Usage:
#   python tools/log_analyzer.py


import json
from pathlib import Path
from collections import Counter
import pandas as pd

LOG_PATH = Path("logs/zero_day_anomalies.json")

def load_logs():
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"No log file found at {LOG_PATH}")
    with open(LOG_PATH) as f:
        return json.load(f)

def summarize_results(log_data):
    all_anomalies = []

    for entry in log_data:
        timestamp = entry.get("timestamp")
        for source, findings in entry.get("results", {}).items():
            for result in findings:
                all_anomalies.append({
                    "timestamp": timestamp,
                    "source": source,
                    "type": result.get("type"),
                    "field": result.get("field", result.get("header", "")),
                    "payload": result.get("payload"),
                    "status_code": result.get("status_code")
                })

    df = pd.DataFrame(all_anomalies)

    if df.empty:
        print("No anomalies found.")
        return

    print("\nAnomaly Counts by Type:")
    print(df["type"].value_counts())

    print("\nTop Payloads:")
    print(df["payload"].value_counts().head(5))

    print("\nScan Timestamps:")
    print(df["timestamp"].value_counts().head(3))

if __name__ == "__main__":
    logs = load_logs()
    summarize_results(logs)
