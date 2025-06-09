# Purpose:
#   Orchestrate the zero-day scanning pipeline across web apps, APIs, and binaries.
#   Runs fuzzers and logs any anomalies using a consistent structure.

# Requirements:
#   pip install requests beautifulsoup4
#
# Usage:
#   python scripts/zero_day_scanner.py

import os
import json
from datetime import datetime
from tools import web_fuzzer  

LOG_PATH = "logs/anomalies.log"

def log_anomalies(target, category, findings):
    """
    Append structured anomaly findings to a persistent log file.
    Each entry includes a timestamp, target info, module category, and findings.
    """
    if not findings:
        return

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "target": target,
        "category": category,
        "findings": findings
    }

    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(json.dumps(entry) + "\n")

    print(f"[+] Logged {len(findings)} anomalies from {category} module.")

def scan_target(target_url):
    """
    Run the zero-day discovery tools against the given target URL or path.
    Currently supports: Web app fuzzing
    """
    print(f"\nScanning target: {target_url}")

    web_results = web_fuzzer.run_web_fuzzer(target_url)
    findings = web_results["header_anomalies"] + web_results["form_anomalies"]
    log_anomalies(target_url, "web", findings)

    print("Scan complete.")

if __name__ == "__main__":
    # Known testable targets
    targets = [
        "https://demo.testfire.net",                              # Web application
        "https://api.restful-booker.herokuapp.com/booking",       # REST API (to be handled in api_fuzzer.py)
        "/usr/bin/file"                                           # Native binary (for binary_fuzzer.py)
    ]

    for target in targets:
        scan_target(target)
