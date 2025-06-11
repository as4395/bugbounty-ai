# Purpose:
#   Generate bug reports from scan findings and save them as text and CSV.

import json
import pandas as pd

def load_findings(filename):
    print(f"Loading findings from {filename}...")
    with open(filename, 'r') as file:
        return json.load(file)

def generate_report(findings):
    print("Generating text report...")
    lines = ["Bug Bounty Report", "==================="]
    for item in findings:
        lines.append(f"IP: {item['ip']} - Ports: {item['nmap']['nmap_ports']}")
    return '\n'.join(lines)

def save_report(text, filename):
    print(f"Saving text report to {filename}...")
    with open(filename, 'w') as file:
        file.write(text)

def save_csv(findings, filename):
    print(f"Saving CSV report to {filename}...")
    df = pd.DataFrame(findings)
    df.to_csv(filename, index=False)

def main():
    findings = load_findings('data/processed/findings.json')
    report_text = generate_report(findings)
    save_report(report_text, 'reports/report.txt')
    save_csv(findings, 'reports/report.csv')
    print("Report generation completed.")

if __name__ == "__main__":
    main()
