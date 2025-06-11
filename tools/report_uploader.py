# Purpose:
#   Upload validated bug bounty reports to supported platforms or assist with manual submission.

# Requirements:
#   pip install requests

# Usage:
#   from tools.report_uploader import upload_report
#   upload_report("submissions/final_submission.txt", platform="hackerone")

import webbrowser
from pathlib import Path
import requests

SUPPORTED_PLATFORMS = {
    "hackerone": "https://hackerone.com/",
    "bugcrowd": "https://bugcrowd.com/",
    "intigriti": "https://app.intigriti.com/"
}

def upload_report(report_path, platform="hackerone", dry_run=True):
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform}")

    report_file = Path(report_path)
    if not report_file.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")

    with open(report_file, "r") as f:
        report_content = f.read()

    print(f"[+] Preparing to submit report to {platform.title()}...")

    if dry_run:
        print("[*] Dry run mode: launching submission page.")
        print(report_content[:1000])  # Preview first 1000 chars
        webbrowser.open(SUPPORTED_PLATFORMS[platform])
    else:
        print("[!] API upload not implemented — defaulting to manual workflow.")

def list_supported_platforms():
    return list(SUPPORTED_PLATFORMS.keys())
