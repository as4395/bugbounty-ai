# Purpose:
#   Serve the Bug Bounty AI Web Dashboard and provide real-time scanning and reporting endpoints.

# Requirements:
#   pip install flask pandas requests

# Usage:
#   python web_dashboard.py
#   Then open: http://localhost:8000

from flask import Flask, request, jsonify, render_template
from pathlib import Path
import json
import datetime

# Tool integrations
from tools.web_fuzzer import run_web_fuzzer
from tools.api_fuzzer import run_api_fuzzer
from tools.anomaly_ranker import rank_anomalies

# Setup
app = Flask(__name__, static_folder="web/static", template_folder="web/templates")

REPORTS_DIR = Path("submissions")
REPORTS_DIR.mkdir(exist_ok=True)

def save_report(target, report_data):
    """Save the scan result to a JSON file."""
    filename = REPORTS_DIR / f"{target.replace('.', '_')}.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=2)

def load_report(target):
    """Load a saved report."""
    filename = REPORTS_DIR / f"{target.replace('.', '_')}.json"
    if filename.exists():
        with open(filename) as f:
            return json.load(f)
    return None

@app.route("/")
def index():
    """Serve frontend dashboard."""
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    """Trigger a web/API fuzz scan and return ranked anomalies."""
    data = request.get_json()
    target = data.get("target", "").strip()

    if not target:
        return jsonify({"error": "Target is required."}), 400

    # Run fuzzers
    web_results = run_web_fuzzer(target)
    api_results = run_api_fuzzer(target, method="GET")  # You can extend this dynamically

    # Merge all anomalies
    all_anomalies = (
        web_results.get("anomalies", []) +
        api_results.get("query_param_anomalies", []) +
        api_results.get("header_anomalies", []) +
        api_results.get("json_body_anomalies", [])
    )

    # Rank anomalies
    ranked = rank_anomalies(all_anomalies)

    # Package results
    output = {
        "target": target,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "web_anomalies": web_results,
        "api_anomalies": api_results,
        "ranked": ranked
    }

    save_report(target, output)

    return jsonify({"message": f"Scan complete for {target}", "result": output})

@app.route("/report")
def report():
    """Retrieve previously saved scan report."""
    target = request.args.get("ip", "").strip()
    if not target:
        return jsonify({"error": "Target is required."}), 400

    report = load_report(target)
    if report:
        return jsonify(report)
    return jsonify({"error": f"No report found for {target}."}), 404

if __name__ == "__main__":
    app.run(port=8000, debug=True)
