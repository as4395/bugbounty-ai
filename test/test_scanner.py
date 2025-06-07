# Purpose:
# Unit tests for scanning functions using Nmap and Shodan.

import json
import os
# The test file is importing these functions from the scanner.py file inside the scripts folder.
from scripts.scanner import save_findings, is_blacklisted

def test_scan_with_nmap():
    # Run a scan with a sample IP
    result = scan_with_nmap("192.0.2.1")
    assert isinstance(result, dict)
    assert result["ip"] == "192.0.2.1"
    assert "open_ports" in result
    assert isinstance(result["open_ports"], list)

def test_lookup_with_shodan():
    # Run a lookup with a sample IP
    result = lookup_with_shodan("192.0.2.2")
    assert isinstance(result, dict)
    assert result["ip"] == "192.0.2.2"
    assert "shodan_info" in result

def test_save_findings(tmp_path):
    # Create mock scan results
    findings = [
        {
            "ip": "192.0.2.3",
            "nmap": {"ip": "192.0.2.3", "open_ports": [80, 443]},
            "shodan": {"ip": "192.0.2.3", "shodan_info": "dummy"}
        }
    ]
    file_path = tmp_path / "findings.json"
    save_findings(findings, file_path)

    # Verify file contents
    with open(file_path, "r") as f:
        loaded = json.load(f)
        assert loaded[0]["ip"] == "192.0.2.3"
        assert "nmap" in loaded[0]
        assert "shodan" in loaded[0]
