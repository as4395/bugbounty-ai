# Purpose:
#   Generate an HTML summary report of vulnerabilities and anomalies for review or submission.

# Requirements:
#   pip install jinja2

# Usage:
#   from tools.report_generator import generate_html_report
#   generate_html_report(anomalies, output_path="reports/summary_report.html")

from jinja2 import Template
from datetime import datetime
from pathlib import Path

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bug Bounty Report Summary</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 8px 12px; border: 1px solid #ccc; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Bug Bounty Report Summary</h1>
    <p>Generated on {{ timestamp }}</p>

    {% if findings %}
    <table>
        <thead>
            <tr>
                <th>Type</th>
                <th>Vector</th>
                <th>Payload</th>
                <th>Status Code</th>
            </tr>
        </thead>
        <tbody>
            {% for item in findings %}
            <tr>
                <td>{{ item.get("type", "N/A") }}</td>
                <td>{{ item.get("field") or item.get("header") or "N/A" }}</td>
                <td>{{ item.get("payload", "N/A") }}</td>
                <td>{{ item.get("status_code", "N/A") }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No findings to report.</p>
    {% endif %}
</body>
</html>
"""

def generate_html_report(findings, output_path="reports/summary_report.html"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rendered = Template(HTML_TEMPLATE).render(findings=findings, timestamp=timestamp)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[+] HTML report generated: {output_file}")
