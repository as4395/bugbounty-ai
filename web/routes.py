# Purpose:
# Define Flask routes for scan and report view.

from flask import request, jsonify, render_template
import os
import json

def register_routes(app):
    DATA_PATH = "data/processed/findings.json"

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/scan", methods=["POST"])
    def scan():
        data = request.get_json()
        target = data.get("target")

        if not target:
            return jsonify({"error": "Missing target"}), 400

        # Dummy scan result — replace with real scanner call
        scan_result = {
            "ip": target,
            "ports": [80, 443, 8080],
            "status": "Scan completed"
        }

        # Save result
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w") as f:
            json.dump([scan_result], f, indent=2)

        return jsonify(scan_result)

    @app.route("/report", methods=["GET"])
    def report():
        ip = request.args.get("ip")
        if not ip:
            return jsonify({"error": "Missing IP"}), 400

        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "No scan data available"}), 404

        with open(DATA_PATH, "r") as f:
            data = json.load(f)

        report = next((entry for entry in data if entry["ip"] == ip), None)

        if not report:
            return jsonify({"error": "No report found for given IP"}), 404

        return jsonify(report)
