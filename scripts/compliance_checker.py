# Purpose:
#   Check reports for compliance with platform rules.

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

    blacklist_ips = rules.get('blacklist_ips', [])
    blacklist_domains = rules.get('blacklist_domains', [])

    for _, row in report_df.iterrows():
        domain = row.get('domain', '')
        ip = row.get('ip', '')

        if ip and ip in blacklist_ips:
            flagged.append(f"IP: {ip}")
        if domain and any(bad_domain in domain for bad_domain in blacklist_domains):
            flagged.append(f"Domain: {domain}")

    return flagged

def main():
    rules = load_rules('configs/platform_rules.yaml')
    report_df = load_report('reports/report.csv')
    flagged_items = check_compliance(report_df, rules)

    if flagged_items:
        print("Non-compliant items found:")
        for item in flagged_items:
            print(f"- {item}")
    else:
        print("All reports compliant.")
    print("Compliance check completed.")

if __name__ == "__main__":
    main()
