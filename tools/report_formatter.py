# Purpose:
# Format scan results into clean summaries for LLMs or reports.

def format_single_entry(entry):
    ip = entry.get('ip', 'Unknown')
    open_ports = entry.get('open_ports', [])
    org = entry.get('organization', 'N/A')
    isp = entry.get('isp', 'N/A')
    country = entry.get('country', 'N/A')
    hostnames = ', '.join(entry.get('hostnames', []))

    summary = (
        f"Target: {ip}\n"
        f"Open Ports: {', '.join(str(p) for p in open_ports) if open_ports else 'None'}\n"
        f"Organization: {org}\n"
        f"ISP: {isp}\n"
        f"Country: {country}\n"
        f"Hostnames: {hostnames if hostnames else 'None'}\n"
        "----------------------------"
    )
    return summary

def format_all(entries):
    return "\n".join([format_single_entry(e) for e in entries])
