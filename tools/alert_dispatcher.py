# Purpose:
#   Dispatch alerts when critical anomalies (score ≥ threshold) are found in zero-day scan logs.
#   Supports terminal output, and can be extended to email, Slack, and generic webhooks.

# Requirements:
#   pip install pandas requests

# Usage:
#   python tools/alert_dispatcher.py

import json
import smtplib
import requests
import pandas as pd
from email.message import EmailMessage
from pathlib import Path

LOG_PATH = Path("logs/zero_day_anomalies.json")
THRESHOLD = 5

# Alert Configuration

EMAIL_ENABLED = True        # Set to False to disable email alerts
SLACK_ENABLED = True        # Set to False to disable Slack alerts
WEBHOOK_ENABLED = True      # Set to False to disable custom webhook alerts

# Email alert settings (for production use, store secrets in environment variables or config file)
EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",             # SMTP server (Gmail used as example)
    "smtp_port": 465,                            # SMTP SSL port
    "sender_email": "your_email@gmail.com",      # REQUIRED: Replace with your sender email
    "sender_password": "your_app_password",      # REQUIRED: Replace with your app-specific password 
    "recipient_email": "recipient@example.com"   # REQUIRED: Replace with the recipient email address
}

# Slack webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"  # REQUIRED: Replace with your actual Slack Incoming Webhook URL

# Generic webhook
GENERIC_WEBHOOK_URL = "https://example.com/alert"  # REQUIRED: Replace with your webhook endpoint

def load_anomalies():
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"Log file not found: {LOG_PATH}")
    with open(LOG_PATH) as f:
        return json.load(f)

def flatten_and_score(logs):
    rows = []
    for entry in logs:
        ts = entry.get("timestamp")
        for source, items in entry.get("results", {}).items():
            for item in items:
                row = {
                    "timestamp": ts,
                    "source": source,
                    "type": item.get("type", ""),
                    "field": item.get("field", item.get("header", "")),
                    "payload": item.get("payload", ""),
                    "status_code": item.get("status_code", 0),
                    "error": item.get("error", "")
                }
                row["score"] = score(row)
                rows.append(row)
    return pd.DataFrame(rows)

def score(row):
    s = 0
    if row["status_code"] and row["status_code"] >= 500:
        s += 3
    elif row["status_code"] >= 400:
        s += 1
    if "traceback" in str(row["error"]).lower() or "segfault" in str(row["error"]).lower():
        s += 3
    elif any(x in str(row["error"]).lower() for x in ["error", "invalid", "undefined"]):
        s += 2
    if row["type"] == "json_body":
        s += 2
    elif row["type"] == "header":
        s += 1
    return s

def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_SETTINGS["sender_email"]
        msg["To"] = EMAIL_SETTINGS["recipient_email"]
        msg.set_content(body)

        with smtplib.SMTP_SSL(EMAIL_SETTINGS["smtp_server"], EMAIL_SETTINGS["smtp_port"]) as smtp:
            smtp.login(EMAIL_SETTINGS["sender_email"], EMAIL_SETTINGS["sender_password"])
            smtp.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print(f"Email alert failed: {e}")

def send_slack_alert(message):
    try:
        res = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if res.status_code != 200:
            print(f"Slack alert failed: {res.text}")
        else:
            print("Slack alert sent.")
    except Exception as e:
        print(f"Slack alert error: {e}")

def send_generic_webhook(payload):
    try:
        res = requests.post(GENERIC_WEBHOOK_URL, json=payload)
        if res.status_code >= 400:
            print(f"Webhook alert failed: {res.text}")
        else:
            print("Webhook alert sent.")
    except Exception as e:
        print(f"Generic webhook error: {e}")

def dispatch_alerts(df):
    critical = df[df["score"] >= THRESHOLD]
    if critical.empty:
        print("No critical anomalies detected.")
        return

    print("\nCritical Anomalies Detected:")
    print(critical[["timestamp", "source", "type", "field", "score"]])

    body = critical.to_string(index=False)

    if EMAIL_ENABLED:
        send_email("Critical Anomaly Detected", body)
    if SLACK_ENABLED:
        send_slack_alert(f"Critical anomalies found:\n{body}")
    if WEBHOOK_ENABLED:
        send_generic_webhook(payload={"alerts": critical.to_dict(orient="records")})

def main():
    logs = load_anomalies()
    df = flatten_and_score(logs)
    dispatch_alerts(df)

if __name__ == "__main__":
    main()
