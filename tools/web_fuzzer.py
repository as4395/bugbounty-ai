# Purpose:
# Perform fuzz testing against web application URLs by injecting payloads into GET parameters.
# Detects anomalies in responses that may indicate input validation issues or unhandled exceptions.

# Requirements:
# pip install requests

# Usage:
# from tools.web_fuzzer import run_web_fuzzer
#
# results = run_web_fuzzer("http://example.com/search?q=FUZZ")

import requests

FUZZ_PAYLOADS = [
    "' OR '1'='1",
    "<script>alert(1)</script>",
    "../../../../etc/passwd",
    "{{7*7}}",
    "%00",
    "'; DROP TABLE users; --"
]

def is_anomalous(response):
    if response.status_code >= 500:
        return True
    for sig in ["error", "exception", "traceback", "not allowed", "invalid", "unexpected"]:
        if sig in response.text.lower():
            return True
    return False

def run_web_fuzzer(url_template):
    if "FUZZ" not in url_template:
        raise ValueError("URL must contain 'FUZZ' as a placeholder.")

    session = requests.Session()
    anomalies = []

    for payload in FUZZ_PAYLOADS:
        test_url = url_template.replace("FUZZ", payload)
        try:
            response = session.get(test_url, timeout=5)
            if is_anomalous(response):
                anomalies.append({
                    "url": test_url,
                    "payload": payload,
                    "status_code": response.status_code
                })
        except requests.RequestException as e:
            anomalies.append({
                "url": test_url,
                "payload": payload,
                "error": str(e),
                "status_code": None
            })

    return anomalies
