# Purpose:
#   Scan approved targets using real Nmap and Shodan, focusing on top 100 common ports.

import csv
import json
import time
import yaml
from tools.nmap_client import run_nmap_scan
from tools.shodan_client import run_shodan_lookup

def load_rules(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def is_blacklisted(domain, rules):
    return any(bad in domain for bad in rules.get('blacklist_domains', []))

def save_findings(findings, filename):
    print(f"Saving findings to {filename}...")
    with open(filename, 'w') as file:
        json.dump(findings, file, indent=2)

def main():
    rules = load_rules('configs/platform_rules.yaml')
    findings = []

    with open('data/raw/asset_targets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            domain = row['domain']
            if is_blacklisted(domain, rules):
                print(f"Skipping blacklisted domain: {domain}")
                continue

            nmap_result = run_nmap_scan(domain)
            shodan_result = run_shodan_lookup('YOUR_SHODAN_API_KEY', domain)

            combined = {
                'domain': domain,
                'nmap': nmap_result,
                'shodan': shodan_result
            }
            findings.append(combined)

            time.sleep(1)  

    save_findings(findings, 'data/processed/findings.json')
    print("Scanning completed.")

if __name__ == "__main__":
    main()
