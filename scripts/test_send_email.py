import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# Config
EMAIL_USER = "cosdaneelolivaw@gmail.com"
EMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD")
TARGET_EMAIL = "jason@crossfitblaze.com"

def send_test_email():
    if not EMAIL_PASS:
        print("ERROR: GMAIL_APP_PASSWORD not set")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"[HEALTH CHECK] Email automation test - {today}"
    body = f"""Daily email automation health check.
Date: {today}
Sender: {EMAIL_USER}
Status: System Check

This is a test email sent from the OpenClaw daily health check script."""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = TARGET_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("SUCCESS")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    send_test_email()
