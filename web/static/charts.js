// Purpose: Render training or fuzzing metrics using Chart.js

export function renderLineChart(ctx, labels, data, label = "Metric") {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        borderColor: "blue",
        fill: false,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Index"
          }
        },
        y: {
          title: {
            display: true,
            text: label
          }
        }
      }
    }
  });
}
