import smtplib
from email.mime.text import MIMEText
from config.config import settings

def send_verification_email(to_email, verification_url):
    """Sends verification email
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = settings.sender_email
    sender_password = settings.sender_password

    msg = MIMEText(f"Click the link to verify your email: {verification_url}")
    msg["Subject"] = "Verify Your Email"
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())