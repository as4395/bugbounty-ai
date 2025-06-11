# Purpose:
#   Export zero-day anomaly results from logs/zero_day_anomalies.json into CSV or simplified JSON format.

# Requirements:
#   pip install pandas

# Usage:
#   python tools/result_exporter.py

import json
import pandas as pd
from pathlib import Path

INPUT_LOG = Path("logs/zero_day_anomalies.json")
EXPORT_DIR = Path("reports/")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def flatten_log_entry(entry):
    flattened = []
    timestamp = entry.get("timestamp")
    for source, results in entry.get("results", {}).items():
        for item in results:
            flattened.append({
                "timestamp": timestamp,
                "source": source,
                "type": item.get("type", ""),
                "field": item.get("field", item.get("header", "")),
                "payload": item.get("payload", ""),
                "status_code": item.get("status_code", ""),
                "error": item.get("error", "")
            })
    return flattened

def export_to_csv(data):
    df = pd.DataFrame(data)
    csv_path = EXPORT_DIR / "flattened_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Exported to: {csv_path}")

def export_to_json(data):
    json_path = EXPORT_DIR / "flattened_results.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported to: {json_path}")

def main():
    if not INPUT_LOG.exists():
        print(f"Log file not found: {INPUT_LOG}")
        return

    with open(INPUT_LOG) as f:
        raw = json.load(f)

    all_results = []
    for entry in raw:
        all_results.extend(flatten_log_entry(entry))

    if not all_results:
        print("No results to export.")
        return

    export_to_csv(all_results)
    export_to_json(all_results)

if __name__ == "__main__":
    main()
