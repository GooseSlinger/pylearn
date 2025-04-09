import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from schemas.BaseSchema import ResponseMessage

def send_email(user_email: str, message: str, title: str): 
    sender_email = "test@example.com"

    msg = MIMEMultipart()
    msg['from'] = sender_email
    msg['to'] = user_email
    msg['Subject'] = title

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('localhost', 1025)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")