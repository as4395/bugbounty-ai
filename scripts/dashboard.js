// Purpose: Fetch and visualize training metrics (reward, loss, epsilon) using Chart.js.
// This file is loaded by dashboard.html via <script src="/dashboard.js">

async function renderCharts() {
    const response = await fetch("/api/enhanced-log");
    const data = await response.json();

    if (!data || !data.reward) {
        alert("Failed to load training data.");
        return;
    }

    const episodes = data.reward.map((_, i) => i + 1);

    const makeChart = (canvasId, label, dataPoints, color) => {
        const ctx = document.getElementById(canvasId).getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: episodes,
                datasets: [{
                    label: label,
                    data: dataPoints,
                    borderColor: color,
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    x: {
                        title: { display: true, text: "Episode" }
                    },
                    y: {
                        title: { display: true, text: label },
                        beginAtZero: true
                    }
                }
            }
        });
    };

    makeChart("rewardChart", "Reward", data.reward, "green");
    makeChart("lossChart", "Loss", data.loss, "red");
    makeChart("epsilonChart", "Epsilon", data.epsilon, "blue");
}

renderCharts();
