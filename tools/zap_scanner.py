# Purpose:
# Use OWASP ZAP to scan a target web application and export alerts using YAML config.

# Make sure to start ZAP with:
# ```bash
# zap.sh -daemon -port 8090 -config api.key=changeme

import time
import json
import yaml
from zapv2 import ZAPv2

def load_config(path='configs/scanner_config.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def scan_target(zap, target_url):
    print(f"[ZAP] Accessing: {target_url}")
    zap.urlopen(target_url)
    time.sleep(2)

    print("[ZAP] Starting active scan...")
    scan_id = zap.ascan.scan(target_url)

    while int(zap.ascan.status(scan_id)) < 100:
        print(f"[ZAP] Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(2)

    print("[ZAP] Scan complete.")
    return zap.core.alerts(baseurl=target_url)

def save_alerts(alerts, filename):
    print(f"[ZAP] Saving alerts to {filename}")
    with open(filename, 'w') as f:
        json.dump(alerts, f, indent=2)

def main():
    config = load_config()
    zap_config = config.get('zap', {})

    api_key = zap_config.get('api_key')
    if not api_key:
        print("[!] API key missing in config. Update scanner_config.yaml with a valid key.")
        return

    port = zap_config.get('port', 8090)
    address = zap_config.get('address', 'localhost')
    output_file = zap_config.get('output_file', 'data/processed/zap_alerts.json')

    proxies = {
        'http': f'http://{address}:{port}',
        'https': f'http://{address}:{port}'
    }

    zap = ZAPv2(apikey=api_key, proxies=proxies)

    target_url = input("Enter target URL for ZAP scan: ").strip()
    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    alerts = scan_target(zap, target_url)
    save_alerts(alerts, output_file)
    print("[ZAP] Scan finished and results saved.")

if __name__ == "__main__":
    main()
