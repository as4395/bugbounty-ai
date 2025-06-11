# Purpose:
#   Perform fuzz testing on RESTful APIs by injecting payloads into URL paths,
#   query parameters, and JSON bodies to discover unexpected behavior or vulnerabilities.

# Requirements:
#   pip install requests

# Usage:
#   from tools.api_fuzzer import run_api_fuzzer
#
#   results = run_api_fuzzer(
#       "https://api.restful-booker.herokuapp.com/booking",
#       method="POST",
#       body_template={"firstname": "FUZZ", "lastname": "Doe"}
#   )


import requests
import json

# Common fuzz payloads for injection
FUZZ_PAYLOADS = [
    "' OR '1'='1",
    "<script>alert(1)</script>",
    "../../../../etc/passwd",
    "{{7*7}}",
    "\\x00",
    "'; DROP TABLE users; --"
]

def fuzz_query_params(session, url):
    # Fuzz query parameters by injecting into a generic 'input' key.
    results = []

    for payload in FUZZ_PAYLOADS:
        test_url = f"{url}?input={payload}"
        response = session.get(test_url)
        if is_anomalous(response):
            results.append({
                "type": "query_param",
                "payload": payload,
                "status_code": response.status_code
            })

    return results

def fuzz_json_body(session, url, method, template):
    # Fuzz JSON payloads by injecting fuzz values into each field in the request body.
    results = []

    for field in template:
        for payload in FUZZ_PAYLOADS:
            mutated = template.copy()
            mutated[field] = payload
            response = session.request(method, url, json=mutated)
            if is_anomalous(response):
                results.append({
                    "type": "json_body",
                    "field": field,
                    "payload": payload,
                    "status_code": response.status_code
                })

    return results

def fuzz_headers(session, url, method):
    # Fuzz common HTTP headers to test for input validation or injection issues.
    results = []
    headers_to_fuzz = ["User-Agent", "Referer", "X-Forwarded-For"]

    for header in headers_to_fuzz:
        for payload in FUZZ_PAYLOADS:
            custom_headers = {header: payload}
            response = session.request(method, url, headers=custom_headers)
            if is_anomalous(response):
                results.append({
                    "type": "header",
                    "header": header,
                    "payload": payload,
                    "status_code": response.status_code
                })

    return results

def is_anomalous(response):
    # Heuristic check for anomalies in API responses.
    error_keywords = [
        "error", "exception", "traceback",
        "not allowed", "fatal", "invalid", "undefined"
    ]
    if response.status_code >= 500:
        return True
    for keyword in error_keywords:
        if keyword.lower() in response.text.lower():
            return True
    return False

def run_api_fuzzer(target_url, method="GET", body_template=None):
    # Runs a full fuzzing routine against a RESTful API endpoint.
    # Args:
    #    target_url (str): The API endpoint URL.
    #    method (str): HTTP method to use (GET, POST, PUT, etc.).
    #    body_template (dict): Optional template for JSON body fuzzing.
    #
    # Returns:
    #    dict: Dictionary with anomaly results from each fuzzing vector.
    
    session = requests.Session()

    print(f"Starting API fuzz test on: {target_url} [{method}]")

    results = {
        "query_param_anomalies": fuzz_query_params(session, target_url),
        "header_anomalies": fuzz_headers(session, target_url, method)
    }

    if body_template and method.upper() in ["POST", "PUT", "PATCH"]:
        results["json_body_anomalies"] = fuzz_json_body(session, target_url, method, body_template)

    print("API fuzzing complete.")
    return results
