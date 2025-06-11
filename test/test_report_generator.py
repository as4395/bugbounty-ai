# Purpose:
#   Unit tests for the report generator functions.

import pandas as pd
# The test file is importing these functions from the report_generator.py file inside the scripts folder.
from scripts.report_generator import generate_report, save_report, save_csv

def test_generate_report():
    # Mock finding based on scanner output structure
    mock_findings = [
        {
            "ip": "192.168.56.10",
            "nmap": {"nmap_ports": [22, 443]},
            "shodan": {"info": "Open ports found"}
        }
    ]
    report_text = generate_report(mock_findings)
    assert "192.168.56.10" in report_text
    assert "22" in report_text
    assert "443" in report_text

def test_save_report(tmp_path):
    # Text to be saved
    text = "Bug Bounty Report\n===================\nTest Entry"
    file_path = tmp_path / "report.txt"

    save_report(text, file_path)

    assert file_path.exists()
    with open(file_path, "r") as f:
        content = f.read()
        assert "Bug Bounty Report" in content
        assert "Test Entry" in content

def test_save_csv(tmp_path):
    # Simulate output as JSON dictionaries
    findings = [
        {
            "ip": "172.16.254.1",
            "nmap": {"nmap_ports": [80, 8080]},
            "shodan": {"info": "Mock info"}
        }
    ]
    file_path = tmp_path / "report.csv"
    save_csv(findings, file_path)

    df = pd.read_csv(file_path)
    assert "ip" in df.columns
    assert df.iloc[0]["ip"] == "172.16.254.1"
