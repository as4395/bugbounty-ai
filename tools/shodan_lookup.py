# Purpose:
#   Lookup a given IP using the Shodan API and return structured metadata.

# Required Installation:
#   pip install shodan

import shodan
import yaml

def load_shodan_key(config_path='configs/scanner_config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('shodan', {}).get('api_key', None)

def lookup_ip(ip_address):
    api_key = load_shodan_key()
    if not api_key:
        print("Shodan API key not found.")
        return {'ip': ip_address, 'error': 'Missing API key'}

    api = shodan.Shodan(api_key)

    try:
        print(f"Querying Shodan for {ip_address}...")
        result = api.host(ip_address)

        open_ports = result.get('ports', [])
        org = result.get('org', 'N/A')
        isp = result.get('isp', 'N/A')
        hostnames = result.get('hostnames', [])
        country = result.get('country_name', 'N/A')

        return {
            'ip': ip_address,
            'open_ports': open_ports,
            'organization': org,
            'isp': isp,
            'hostnames': hostnames,
            'country': country
        }

    except shodan.exception.APIError as e:
        print(f"Shodan API error: {e}")
        return {'ip': ip_address, 'error': str(e)}
