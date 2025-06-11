# Purpose:
#   Perform fuzz testing against web application URLs by injecting payloads into GET parameters.
#   Detects anomalies in responses that may indicate input validation issues or unhandled exceptions.

# Requirements:
#   pip install requests

# Usage:
#   from tools.web_fuzzer import run_web_fuzzer
#   results = run_web_fuzzer("http://example.com/search?q=FUZZ")

import requests

FUZZ_PAYLOADS = [
    "' OR 1=1 --", "<script>alert(1)</script>", "../../etc/passwd", "'; DROP TABLE users; --"
]

def run_web_fuzzer(url):
    results = []

    for payload in FUZZ_PAYLOADS:
        test_url = url.replace("FUZZ", payload)
        try:
            response = requests.get(test_url, timeout=5)
            if is_anomalous(response):
                results.append({
                    "payload": payload,
                    "status_code": response.status_code,
                    "content_snippet": response.text[:200]
                })
        except Exception as e:
            results.append({
                "payload": payload,
                "error": str(e)
            })

    return {
        "target": url,
        "anomalies": results
    }

def is_anomalous(response):
    if response.status_code >= 500:
        return True
    for keyword in ["error", "exception", "fatal", "not allowed"]:
        if keyword in response.text.lower():
            return True
    return False
