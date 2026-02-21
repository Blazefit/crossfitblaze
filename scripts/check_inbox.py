import imaplib
import email
import os
import smtplib
from email.mime.text import MIMEText

# Config
EMAIL_USER = "cosdaneelolivaw@gmail.com"
EMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD")
TARGET_EMAIL = "jason@crossfitblaze.com"

def check_emails():
    try:
        if not EMAIL_PASS:
            return "ERROR: GMAIL_APP_PASSWORD not set"

        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            return "ERROR: Could not search inbox"

        mail_ids = messages[0].split()
        if not mail_ids:
            return "SILENT_OK"

        results = []
        for m_id in mail_ids:
            status, data = mail.fetch(m_id, "(RFC822)")
            if status != "OK":
                continue
            
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg["Subject"]
            from_addr = msg["From"]
            
            # Basic Categorization Logic
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

            cat = "OTHER"
            lower_body = body.lower()
            lower_sub = subject.lower()
            
            if "drop-in" in lower_body or "drop in" in lower_body:
                cat = "DROP-IN"
            elif "trial" in lower_body or "lead" in lower_body or "sign up" in lower_body:
                cat = "TRIAL/LEAD"
            elif "member" in lower_body or "question" in lower_body or "cancel" in lower_body:
                cat = "CLIENT EMAIL"
            elif "promo" in lower_body or "sale" in lower_body or "unsubscribe" in lower_body:
                cat = "PROMO/SPAM"

            results.append({
                "id": m_id,
                "from": from_addr,
                "subject": subject,
                "category": cat,
                "body": body[:200]
            })

        # Summary for Jason
        clients = [r for r in results if r["category"] == "CLIENT EMAIL"]
        leads = [r for r in results if r["category"] == "TRIAL/LEAD"]
        dropins = [r for r in results if r["category"] == "DROP-IN"]
        spams = [r for r in results if r["category"] == "PROMO/SPAM"]

        # 1. Archive Spam/Promos
        for s in spams:
            mail.store(s["id"], '+FLAGS', '\\Deleted')
        mail.expunge()

        # 2. Report if actionable
        report = []
        if clients:
            report.append("📢 **New Client Emails:**")
            for c in clients:
                report.append(f"- From: {c['from']}\n  Sub: {c['subject']}")
        
        if leads:
            report.append("\n🎯 **New Leads/Trials:**")
            for l in leads:
                report.append(f"- From: {l['from']}\n  Sub: {l['subject']}")

        if len(results) >= 10:
            report.append(f"\n⚠️ **High Volume:** {len(results)} total unread emails in inbox.")

        if report:
            return "\n".join(report)
        else:
            return "SILENT_OK"

    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        try:
            mail.logout()
        except:
            pass

if __name__ == "__main__":
    print(check_emails())
