import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

date_str = datetime.now().strftime("%Y-%m-%d")
body = f"""This is an automated health check for your email systems.

Verification of templates and formatting:
- Plain text: Check
- Sender: Daneel (cosdaneelolivaw@gmail.com)
- Target: Jason (jason@crossfitblaze.com)

Automation status: Operational."""

msg = MIMEText(body)
msg["Subject"] = f"[HEALTH CHECK] Email automation test - {date_str}"
msg["From"] = "cosdaneelolivaw@gmail.com"
msg["To"] = "jason@crossfitblaze.com"

password = os.environ.get("GMAIL_APP_PASSWORD") or "your_placeholder_here"

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("cosdaneelolivaw@gmail.com", password)
        server.send_message(msg)
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
    exit(1)
