import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

my_email = "blue.panda070413@gmail.com"
password = os.environ.get("smtplib_password")

def email_sending(to_email, subject, html_content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = my_email
    message["To"] = to_email

    part = MIMEText(html_content, "html")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.ehlo()          
        connection.starttls()     
        connection.ehlo()            
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=message.as_string()
        ) 