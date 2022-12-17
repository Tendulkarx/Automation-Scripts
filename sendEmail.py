import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = os.environ.get("email_user")
password = os.environ.get("email_pass")


# text='Email Body', subject='Notified', from_email=username, to_emails=[username]
def send_email(from_email, to_emails, subject, message_body, html=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    txt_part = MIMEText(message_body, "html")
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, "html")
        msg.attach(html_part)
    msg_str = msg.as_string()

    # login to smtp server
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
