// Purpose: Entry point — wire up DOM interactions and connect UI to API.

import { postScan, fetchReport } from "./api.js";
import { showLoading, renderJSON, renderError } from "./ui.js";
import { sanitizeInput, isValidTarget } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const scanForm = document.getElementById("scan-form");
  const scanResult = document.getElementById("scan-result");

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

    try {
      const result = await postScan(target);
      renderJSON(scanResult, result);
    } catch (err) {
      renderError(scanResult, "Error performing scan.");
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
      const result = await fetchReport(ip);
      renderJSON(reportOutput, result);
    } catch (err) {
      renderError(reportOutput, "Error loading report.");
    }
  });
});
