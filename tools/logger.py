# Purpose:
# Main logging tool for consistent status messages across the project.

import datetime

LOG_FILE = "logs/bugbounty.log"

def log(message, level="INFO", to_file=False):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    label = level.upper()

    # Colored output
    if label == "INFO":
        prefix = f"\033[94m[{label}]\033[0m"
    elif label == "WARNING":
        prefix = f"\033[93m[{label}]\033[0m"
    elif label == "ERROR":
        prefix = f"\033[91m[{label}]\033[0m"
    else:
        prefix = f"[{label}]"

    log_entry = f"{timestamp} {prefix} {message}"
    print(log_entry)

    if to_file:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} [{label}] {message}\n")
