// Purpose: Manage UI rendering and updates to DOM elements.

export function showLoading(element, message = "Loading...") {
  element.textContent = message;
}

export function renderJSON(element, data) {
  element.textContent = JSON.stringify(data, null, 2);
}

export function renderError(element, message = "Something went wrong.") {
  element.textContent = `❌ ${message}`;
}
