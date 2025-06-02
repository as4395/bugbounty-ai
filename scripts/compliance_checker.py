# Purpose:
# Check reports for compliance with platform rules.

import pandas as pd
import yaml

def load_rules(filename):
    print(f"Loading rules from {filename}...")
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def load_report(filename):
    print(f"Loading report from {filename}...")
    return pd.read_csv(filename)

def check_compliance(report_df, rules):
    print("Checking compliance...")
    flagged = []
    blacklist = rules.get('blacklist', [])
    for _, row in report_df.iterrows():
        if row['ip'] in blacklist:
            flagged.append(row['ip'])
    return flagged

def main():
    rules = load_rules('configs/platform_rules.yaml')
    report_df = load_report('reports/report.csv')
    flagged_ips = check_compliance(report_df, rules)
    if flagged_ips:
        print("Non-compliant IPs found:")
        for ip in flagged_ips:
            print(f"- {ip}")
    else:
        print("All reports compliant.")
    print("Compliance check completed.")

if __name__ == "__main__":
    main()
