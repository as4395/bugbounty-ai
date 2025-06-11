// Purpose: General-purpose utility functions.

export function sanitizeInput(input) {
  return input.replace(/[<>]/g, "");
}

export function isValidTarget(target) {
  return typeof target === "string" && target.trim().length > 0;
}
