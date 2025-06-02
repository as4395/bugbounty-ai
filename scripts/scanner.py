# Purpose:
# Scan targets using Nmap and pyshodan, focusing on the top 100 most common ports.

import json

TOP_PORTS = [
    20, 21, 22, 23, 24, 25, 26, 53, 69, 80, 81, 88, 110, 111, 135, 137, 139, 143,
    161, 162, 389, 443, 445, 465, 500, 636, 993, 995, 1025, 1026, 1027, 1028, 1029,
    1030, 1080, 1433, 1521, 1720, 1723, 1900, 3128, 3306, 3389, 5000, 5432, 5800,
    5900, 5901, 6000, 7000, 8000, 8080, 8081, 8443, 8888, 10000, 32768,
    49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49162,
    49163, 49164, 49165, 49166, 49167, 49168, 49169, 49170, 49171, 49172, 49173,
    49174, 49175, 49176, 49177, 49178, 49179, 49180, 49181, 49182, 49183, 49184,
    49185, 49186, 49187, 49188, 49189, 49190, 49191, 49192, 49193, 49194
]

def scan_with_nmap(target):
    print(f"Scanning {target} with Nmap...")
    # Dummy result: Pretend the first five ports are open
    open_ports = TOP_PORTS[:5]
    return {'ip': target, 'open_ports': open_ports}

def lookup_with_shodan(target):
    print(f"Looking up {target} on Shodan...")
    # Dummy result
    return {'ip': target, 'shodan_info': 'Example Shodan data'}

def save_findings(findings, filename):
    print(f"Saving findings to {filename}...")
    with open(filename, 'w') as file:
        json.dump(findings, file, indent=2)

def main():
    targets = ['8.8.8.8', '1.1.1.1']
    all_results = []
    for target in targets:
        nmap_result = scan_with_nmap(target)
        shodan_result = lookup_with_shodan(target)
        combined = {'ip': target, 'nmap': nmap_result, 'shodan': shodan_result}
        all_results.append(combined)
    save_findings(all_results, 'data/processed/findings.json')
    print("Scanning completed.")

if __name__ == "__main__":
    main()
