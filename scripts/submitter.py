# Purpose:
# Prepare bug reports for manual submission to platforms and log prep status.

def load_report(filename):
    print(f"Loading report from {filename}...")
    with open(filename, 'r') as file:
        return file.read()

def prepare_manual_submission(report, filename):
    print(f"Preparing manual submission package in {filename}...")
    with open(filename, 'w') as file:
        file.write("=== MANUAL SUBMISSION REQUIRED ===\n")
        file.write("Please log into the following platforms and submit manually:\n")
        file.write("- HackerOne: https://hackerone.com/ (via program dashboard)\n")
        file.write("- Bugcrowd: https://bugcrowd.com/ (via program dashboard)\n")
        file.write("- Intigriti: https://app.intigriti.com/ (via program dashboard)\n\n")
        file.write("=== REPORT CONTENT ===\n\n")
        file.write(report)

def log_preparation(status, filename):
    print(f"Logging preparation status to {filename}...")
    with open(filename, 'a') as file:
        file.write(f"Preparation status: {status}\n")

def main():
    report = load_report('reports/report.txt')
    prepare_manual_submission(report, 'submissions/final_submission.txt')
    log_preparation('Ready for manual upload', 'logs/submission.log')
    print("Submission package prepared and logged.")

if __name__ == "__main__":
    main()
