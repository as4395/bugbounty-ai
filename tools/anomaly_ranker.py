# Purpose:
#   Analyze and rank anomaly findings from zero-day fuzzing logs by severity.
#   Outputs a ranked list of issues based on vector type, response codes, and error content.

# Requirements:
#   pip install pandas

# Usage:
#   python tools/anomaly_ranker.py

import json
from pathlib import Path
import pandas as pd

INPUT_LOG = Path("logs/zero_day_anomalies.json")

def load_logs():
    if not INPUT_LOG.exists():
        raise FileNotFoundError(f"Log file not found: {INPUT_LOG}")
    with open(INPUT_LOG) as f:
        return json.load(f)

def flatten_entries(logs):
    rows = []
    for entry in logs:
        ts = entry.get("timestamp")
        for source, items in entry.get("results", {}).items():
            for item in items:
                rows.append({
                    "timestamp": ts,
                    "source": source,
                    "type": item.get("type", ""),
                    "field": item.get("field", item.get("header", "")),
                    "payload": item.get("payload", ""),
                    "status_code": item.get("status_code", 0),
                    "error": item.get("error", ""),
                    "raw": item
                })
    return pd.DataFrame(rows)

def score_anomaly(row):
    score = 0
    if row["status_code"] and row["status_code"] >= 500:
        score += 3
    elif row["status_code"] >= 400:
        score += 1

    if "traceback" in str(row["error"]).lower() or "segfault" in str(row["error"]).lower():
        score += 3
    elif any(keyword in str(row["error"]).lower() for keyword in ["error", "invalid", "undefined"]):
        score += 2

    if row["type"] == "json_body":
        score += 2
    elif row["type"] == "header":
        score += 1

    return score

def main():
    logs = load_logs()
    df = flatten_entries(logs)

    if df.empty:
        print("No anomalies to rank.")
        return

    df["severity_score"] = df.apply(score_anomaly, axis=1)
    df_sorted = df.sort_values(by="severity_score", ascending=False)

    print("\nTop Ranked Anomalies:")
    print(df_sorted[["timestamp", "source", "type", "field", "status_code", "severity_score"]].head(10))

    output_path = Path("reports/ranked_anomalies.csv")
    df_sorted.to_csv(output_path, index=False)
    print(f"Full ranked list exported to: {output_path}")
if __name__ == "__main__":
    main()
