# Purpose:
# Define HTTP routes for the Bug Bounty AI Workflow Flask API.

from flask import request, jsonify
from utils import trigger_scan, load_report

def register_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Bug Bounty AI Workflow API is running."})

    @app.route("/status", methods=["GET"])
    def status():
        return jsonify({"status": "online", "phase": "1"})

    @app.route("/scan", methods=["POST"])
    def scan():
        data = request.get_json()
        target = data.get("target")
        if not target:
            return jsonify({"error": "Target not provided."}), 400
        
        result = trigger_scan(target)
        return jsonify({"message": "Scan started", "target": target, "result": result})

    @app.route("/report/<target>", methods=["GET"])
    def get_report(target):
        report_data = load_report(target)
        if report_data is None:
            return jsonify({"error": "Report not found."}), 404
        return jsonify(report_data)
