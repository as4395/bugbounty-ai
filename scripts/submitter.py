# Purpose:
# Submit bug reports to platforms and log submission status.

import requests

def load_report(filename):
    print(f"Loading report from {filename}...")
    with open(filename, 'r') as file:
        return file.read()

def submit_report(report, url):
    print(f"Submitting report to {url}...")
    response = requests.post(url, data={'report': report})
    print(f"Submission response: {response.status_code}")
    return response.status_code

def log_submission(status, filename):
    print(f"Logging status to {filename}...")
    with open(filename, 'a') as file:
        file.write(f"Submission status: {status}\n")

def main():
    report = load_report('reports/report.txt')
    url = 'https://example.com/api/submit'
    status = submit_report(report, url)
    log_submission(status, 'logs/submission.log')
    print("Submission completed.")

if __name__ == "__main__":
    main()
