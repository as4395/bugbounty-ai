# Purpose:
#   Reusable Nmap scanner that runs a top-ports scan on a given IP address.

import subprocess
import yaml

def load_nmap_config(config_path='configs/scanner_config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('nmap', {})

def run_nmap_scan(ip_address):
    config = load_nmap_config()

    top_ports = config.get('top_ports', 100)
    timeout = config.get('timeout', 300)
    arguments = config.get('arguments', '-sS -T4')

    print(f"Scanning {ip_address} with Nmap...")

    # Full Nmap command
    command = f"nmap {arguments} --top-ports {top_ports} {ip_address}"

    try:
        # Run Nmap and capture output
        output = subprocess.check_output(
            command.split(),
            timeout=timeout,
            stderr=subprocess.STDOUT
        ).decode()

        open_ports = []

        # Parse lines for open TCP ports
        for line in output.splitlines():
            if '/tcp' in line and 'open' in line:
                port = line.split('/')[0].strip()
                open_ports.append(int(port))

        return {
            'ip': ip_address,
            'open_ports': open_ports
        }

    except subprocess.CalledProcessError as e:
        print(f"Scan error on {ip_address}: {e.output.decode()}")
        return {'ip': ip_address, 'open_ports': []}

    except subprocess.TimeoutExpired:
        print(f"Scan timed out for {ip_address}")
        return {'ip': ip_address, 'open_ports': []}
