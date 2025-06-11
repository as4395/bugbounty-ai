# Purpose:
#   Flask app to serve the Bug Bounty AI dashboard and handle scan/report requests.

# Requirements:
#   pip install flask

# Usage:
#   python web/app.py
#   Visit http://localhost:5000

from flask import Flask, request, jsonify, render_template
import json
from pathlib import Path
from tools.web_fuzzer import run_web_fuzzer  # Or replace with another scanner if preferred

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    target = data.get("target")

    if not target:
        return jsonify({"error": "No target provided"}), 400

    # Run your scan logic
    results = run_web_fuzzer(target)

    # Save results to JSON file
    save_report(target, results)

    return jsonify(results)

@app.route("/report")
def report():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing IP or domain"}), 400

    report_path = Path(f"submissions/{ip}_report.json")
    if not report_path.exists():
        return jsonify({"error": "Report not found"}), 404

    with open(report_path) as f:
        data = json.load(f)

    return jsonify(data)

def save_report(ip, data):
    """Save scan results to a file for future reference."""
    sanitized_name = ip.replace("/", "_").replace(":", "_")
    output_path = Path(f"submissions/{sanitized_name}_report.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
