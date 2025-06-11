// Purpose: Display in-page alerts for success/failure/info.

export function showAlert(message, type = "info") {
  const alertBox = document.createElement("div");
  alertBox.textContent = message;
  alertBox.className = `alert alert-${type}`;
  document.body.prepend(alertBox);

  setTimeout(() => alertBox.remove(), 3000);
}
