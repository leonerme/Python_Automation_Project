import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import os

# Email account credentials
email_accounts = [
    {"email": "leoner4848@gmail.com", "password": "gwtd ycfw xqyk spmw", "smtp_server": "smtp.gmail.com", "port": 587},
]

# Pre-defined recipient list
recipients = ["tanjeemtahmeed@gmail.com", "tanjeemtahmeed@gmail.com"]

# Pre-defined subject and message
subject = "Scheduled Email"
message = "Hello Everyone," + os.linesep + "Good Evening," + os.linesep + "Today I have prepared the order report for the COL project." + os.linesep + "Here is the URL of the Google sheet:" + os.linesep + "https://docs.google.com/spreadsheets/d/1xeGIR6g2cbpY1ZBQdqm8xArZKJlhrbJctaFJs_rpzkI/edit?gid=1006755034#gid=1006755034" + os.linesep + "Thank you!" + os.linesep + "Best Regards."

def send_email(sender, recipient, subject, message, smtp_server, port, password):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        # Connect to the server and send email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent successfully from {sender} to {recipient}")
    except Exception as e:
        print(f"Failed to send email from {sender}: {e}")

def schedule_emails():
    for account in email_accounts:
        for recipient in recipients:
            send_email(
                sender=account["email"],
                recipient=recipient,
                subject=subject,
                message=message,
                smtp_server=account["smtp_server"],
                port=account["port"],
                password=account["password"],
            )

# Schedule emails every day at 9:00 AM
schedule.every().day.at("16:30").do(schedule_emails)

print("Mail bot running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
