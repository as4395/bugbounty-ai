# Purpose:
# Utility functions to trigger scans and load reports for the web interface.

import json
import os
from pathlib import Path
from scripts.scanner import scan_with_nmap, lookup_with_shodan

REPORTS_DIR = Path("reports")
PROCESSED_DIR = Path("data/processed")

def trigger_scan(target):
    # Run scanners
    nmap_result = scan_with_nmap(target)
    shodan_result = lookup_with_shodan(target)

    # Combine results
    result = {
        "ip": target,
        "nmap": nmap_result,
        "shodan": shodan_result
    }

    # Save raw JSON report
    output_path = PROCESSED_DIR / f"{target}_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    return {"output_file": str(output_path)}

def load_report(target):
    report_path = PROCESSED_DIR / f"{target}_report.json"
    if not report_path.exists():
        return None

    with open(report_path, "r") as f:
        return json.load(f)
