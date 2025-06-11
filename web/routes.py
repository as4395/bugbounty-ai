# Purpose:
#   Define Flask routes for scan and report view.

from flask import request, jsonify, render_template
from web.utils import trigger_scan, load_report

def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/scan", methods=["POST"])
    def scan():
        data = request.get_json()
        target = data.get("target")

        if not target:
            return jsonify({"error": "Missing target"}), 400

        # Run scan and save results
        scan_info = trigger_scan(target)

        # Return confirmation and filename
        return jsonify({
            "ip": target,
            "status": "Scan completed",
            "output_file": scan_info["output_file"]
        })

    @app.route("/report", methods=["GET"])
    def report():
        ip = request.args.get("ip")
        if not ip:
            return jsonify({"error": "Missing IP"}), 400

        report = load_report(ip)
        if not report:
            return jsonify({"error": "No report found for given IP"}), 404

        return jsonify(report)
