# Purpose:
#   Serve live anomaly data (rewards, losses, epsilons, and alerts) to the dashboard via a Flask API.

# Requirements:
#   pip install flask
#
# Usage:
#   python dashboard_api_connector.py
#   Then visit: http://localhost:5002/api/metrics

from flask import Flask, jsonify
from pathlib import Path
import json

app = Flask(__name__)

# Paths to dynamic data logs
REWARD_LOG = Path("logs/training_rewards.json")
LOSS_LOG = Path("logs/training_losses.json")
EPSILON_LOG = Path("logs/epsilon_values.json")
ANOMALY_LOG = Path("logs/anomalies.json")

def load_json_data(path):
    if not path.exists():
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@app.route("/api/metrics")
def get_metrics():
    return jsonify({
        "rewards": load_json_data(REWARD_LOG),
        "losses": load_json_data(LOSS_LOG),
        "epsilons": load_json_data(EPSILON_LOG),
        "anomalies": load_json_data(ANOMALY_LOG)
    })

@app.route("/")
def index():
    return jsonify({"message": "Bug Bounty AI Dashboard API is running."})

if __name__ == "__main__":
    app.run(port=5002)
