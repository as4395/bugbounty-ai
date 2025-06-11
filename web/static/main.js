// Purpose: Entry point — trigger UI + scan/report flows

import { postScan, fetchReport } from "./api.js";
import { showLoading, renderJSON, renderError, renderAnomalies } from "./ui.js";
import { sanitizeInput, isValidTarget } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const scanForm = document.getElementById("scan-form");
  const scanResult = document.getElementById("scan-result");
  const anomaliesList = document.getElementById("anomalies-list");

  const reportForm = document.getElementById("report-form");
  const reportOutput = document.getElementById("report-output");

  scanForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const rawInput = document.getElementById("target-ip").value;
    const target = sanitizeInput(rawInput);
    if (!isValidTarget(target)) {
      renderError(scanResult, "Please enter a valid target.");
      return;
    }
    showLoading(scanResult, "Scanning...");
    anomaliesList.textContent = "Waiting for results...";
    try {
      const res = await postScan(target);
      renderJSON(scanResult, res.result);
      renderAnomalies(anomaliesList, res.result.ranked);
    } catch (err) {
      renderError(scanResult, "Error performing scan.");
      anomaliesList.textContent = "";
    }
  });

  reportForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const rawInput = document.getElementById("report-ip").value;
    const ip = sanitizeInput(rawInput);
    if (!isValidTarget(ip)) {
      renderError(reportOutput, "Please enter a valid IP or domain.");
      return;
    }
    showLoading(reportOutput, "Loading report...");
    try {
      const res = await fetchReport(ip);
      renderJSON(reportOutput, res);
    } catch (err) {
      renderError(reportOutput, "Error loading report.");
    }
  });
});
