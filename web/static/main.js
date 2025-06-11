// static/main.js — handles form interactions and fetches

document.addEventListener("DOMContentLoaded", () => {
  const scanForm = document.getElementById("scan-form");
  const scanResult = document.getElementById("scan-result");

  const reportForm = document.getElementById("report-form");
  const reportOutput = document.getElementById("report-output");

  // Handle Scan Form Submission
  scanForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const target = document.getElementById("target-ip").value.trim();
    if (!target) return (scanResult.textContent = "Please enter a target.");

    scanResult.textContent = "🔍 Scanning...";
    try {
      const res = await fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target })
      });
      const data = await res.json();
      scanResult.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      scanResult.textContent = "❌ Error performing scan.";
    }
  });

  // Handle Report Viewer
  reportForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ip = document.getElementById("report-ip").value.trim();
    if (!ip) return (reportOutput.textContent = "Please enter an IP.");

    reportOutput.textContent = "📄 Loading report...";
    try {
      const res = await fetch(`/report?ip=${encodeURIComponent(ip)}`);
      const data = await res.json();
      reportOutput.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      reportOutput.textContent = "❌ Error loading report.";
    }
  });
});
