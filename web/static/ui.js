// Purpose: Manage UI rendering and updates to DOM elements

export function showLoading(element, message = "Loading...") {
  element.textContent = message;
}

export function renderJSON(element, data) {
  element.textContent = JSON.stringify(data, null, 2);
}

export function renderError(element, message = "Something went wrong.") {
  element.textContent = message;
}

// Render anomaly list
export function renderAnomalies(container, anomalies) {
  if (!Array.isArray(anomalies) || anomalies.length === 0) {
    container.textContent = "No anomalies detected.";
    return;
  }
  container.innerHTML = "";
  const list = document.createElement("ul");
  anomalies.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>[${item.score}]</strong> ${item.type} – ${item.payload || item.url || item.field}`;
    list.appendChild(li);
  });
  container.appendChild(list);
}
