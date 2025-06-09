# Purpose: Serve the enhanced DQN training dashboard with reward, loss, and epsilon visualizations.

# Requirements:
#   pip install flask
#
# Usage:
#   Run the script:
#     python scripts/dashboard.py
#
#   Then open in your browser:
#     http://localhost:5001

from flask import Flask, send_from_directory, jsonify
import json
from pathlib import Path

app = Flask(__name__)

# Log file path
LOG_PATH = Path("logs/enhanced_training_log.json")
# HTML and JS assets live in this directory
SCRIPTS_PATH = Path("scripts")

@app.route("/")
def serve_dashboard():
    """Serve the main dashboard HTML page."""
    return send_from_directory(SCRIPTS_PATH.resolve(), "dashboard.html")

@app.route("/dashboard.js")
def serve_js():
    """Serve the dashboard JavaScript file."""
    return send_from_directory(SCRIPTS_PATH.resolve(), "dashboard.js")

@app.route("/api/enhanced-log")
def serve_log():
    """Serve reward, loss, and epsilon logs as JSON."""
    if not LOG_PATH.exists():
        return jsonify({"error": "Log file not found."}), 404
    with open(LOG_PATH, "r") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(port=5001)
