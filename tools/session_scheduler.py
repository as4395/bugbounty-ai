# Purpose:
#   Automate scheduled execution of the zero_day_scanner to continuously monitor targets.
#   The session scheduler an be triggered manually or via cron/systemd/task scheduler.

# Requirements:
#   Python standard library only

# Usage:
#   python tools/session_scheduler.py
#   (Or run via cron: `@daily python /path/to/session_scheduler.py`)

import time
import subprocess
from datetime import datetime

SCAN_INTERVAL_SECONDS = 86400  # 1 day (24 * 60 * 60)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_scan():
    log("Starting zero-day scan...")
    result = subprocess.run(["python", "tools/zero_day_scanner.py"])
    log(f"Scan completed with exit code {result.returncode}")

def main():
    while True:
        run_scan()
        log(f"Sleeping for {SCAN_INTERVAL_SECONDS} seconds...")
        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
