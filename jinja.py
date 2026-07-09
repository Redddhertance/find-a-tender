import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv
load_dotenv()

env = Environment(loader=FileSystemLoader('templates'))

template = env.get_template('template.html')

def send_alert(contract_title, value_amount, buyer_name):
    html_content = template.render(
        contract_title=contract_title,
        value_amount=value_amount,
        buyer_name=buyer_name
    )

    msg = EmailMessage()
    msg['Subject'] = 'New Contract Alert: {}'.format(contract_title)
    msg['From'] = os.getenv('sender_email', '')
    msg['To'] = os.getenv('user_email', '')

    msg.set_content('This is a plain text version of the email.')
    msg.add_alternative(html_content, subtype='html')

    #smtp
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 #TLS port

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            reciever = os.getenv('user_email')
            sender = os.getenv('sender_email')
            password = os.getenv('passkey')

            if sender is None or password is None:
                raise ValueError("Sender email or password is not set in environment variables.")
            print(f"DEBUG Sender: '{sender}'")
            print(f"DEBUG Receiver: '{reciever}'")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls() #encryption
                #send
                server.login(sender, password)
                server.send_message(msg)
                print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")