# Purpose:
# Perform basic fuzz testing on local native binaries by feeding mutated input via stdin.
# Detect crashes, hangs, or unexpected behavior based on exit codes and stderr output.

# Requirements:
# No external packages — uses Python standard library only.

# Usage:
# from tools.binary_fuzzer import run_binary_fuzzer
#
# results = run_binary_fuzzer("/usr/bin/file")
# for r in results:
#     if r["crashed"]:
#         print("[CRASH] Input caused failure:", r["input"][:50])

import subprocess
import os

# Common fuzz payloads for testing binary robustness
FUZZ_INPUTS = [
    b"A" * 100,                      # Short buffer
    b"A" * 1000,                     # Long buffer
    b"%x" * 100,                     # Format string attack
    b"\x00\xff\xfe\xfd",             # Non-printable bytes
    b"<script>alert(1)</script>",    # Script injection
    b"../../../../etc/passwd",       # Directory traversal
    b"\x41" * 1024                   # 1 KB of 'A's
]

def run_fuzz_once(binary_path, input_data):
    # Runs the binary with one fuzzed input and captures its behavior.
    try:
        result = subprocess.run(
            [binary_path],
            input=input_data,
            capture_output=True,
            timeout=3,
            check=False
        )
        crashed = (
            result.returncode != 0 or 
            b"error" in result.stderr.lower() or 
            b"segfault" in result.stderr.lower()
        )
        return {
            "input": repr(input_data),
            "stdout": result.stdout.decode(errors="ignore"),
            "stderr": result.stderr.decode(errors="ignore"),
            "returncode": result.returncode,
            "crashed": crashed
        }
    except subprocess.TimeoutExpired:
        return {
            "input": repr(input_data),
            "stdout": "",
            "stderr": "Timeout",
            "returncode": None,
            "crashed": True
        }

def run_binary_fuzzer(binary_path):
    # Runs a fuzzing campaign against the specified binary.
    #
    # Args:
    #   binary_path (str): Absolute or relative path to binary executable.
    #
    # Returns:
    #   list: List of results per fuzz input, including crash status.
    
    print(f"Starting binary fuzzing on: {binary_path}")

    if not os.path.isfile(binary_path) or not os.access(binary_path, os.X_OK):
        raise FileNotFoundError(f"Binary not found or not executable: {binary_path}")

    results = []

    for fuzz in FUZZ_INPUTS:
        result = run_fuzz_once(binary_path, fuzz)
        results.append(result)
        if result["crashed"]:
            print(f"[!] Crash detected with input: {fuzz[:20]}...")

    print("Binary fuzzing complete.")
    return results
