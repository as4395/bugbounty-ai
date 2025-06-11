// Purpose: Handle all API interactions with the Flask backend.

export async function postScan(target) {
  const res = await fetch("/scan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target })
  });
  return res.json();
}

export async function fetchReport(ip) {
  const res = await fetch(`/report?ip=${encodeURIComponent(ip)}`);
  return res.json();
}
