# Purpose: Launch a local web dashboard that plots training reward progression using Flask and Chart.js.

from flask import Flask, jsonify
import json
from pathlib import Path

# Requirements:
# ```bash
# pip install flask
#
# Usage: 
# Run the script:
# ```bash 
# python scripts/dashboard.py
#
# Then open:
# http://localhost:5001

app = Flask(__name__)
LOG_PATH = Path("logs/training_rewards.json")

@app.route("/api/rewards")
def get_rewards():
    """Serve training rewards as JSON."""
    if not LOG_PATH.exists():
        return jsonify({"error": "Log file not found."}), 404
    with open(LOG_PATH) as f:
        rewards = json.load(f)
    return jsonify(rewards=rewards)

@app.route("/")
def index():
    # Serve the main dashboard page with a reward line chart.
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DQN Training Dashboard</title>
    </head>
    <body>
        <h2>DQN Reward Over Time</h2>
        <canvas id="chart" width="800" height="400"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            fetch("/api/rewards")
              .then(res => res.json())
              .then(data => {
                const ctx = document.getElementById("chart").getContext("2d");
                new Chart(ctx, {
                  type: "line",
                  data: {
                    labels: data.rewards.map((_, i) => i + 1),
                    datasets: [{
                      label: "Reward",
                      data: data.rewards,
                      borderColor: "blue",
                      fill: false,
                      tension: 0.1
                    }]
                  },
                  options: {
                    scales: {
                      x: { title: { display: true, text: "Episode" } },
                      y: { title: { display: true, text: "Reward" } }
                    }
                  }
                });
              });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(port=5001)
