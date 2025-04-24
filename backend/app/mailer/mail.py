import smtplib, secrets, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Template

from config import MAIL_KEY

verification_codes = {}

def load_key_to_email():
    load_dotenv()

def confirmation_code():
    confirmation_code = str(secrets.randbelow(10 ** 6)).zfill(6)
    return confirmation_code

def clean_expired_codes():
    current_time = time.time()
    expired_keys = [email for email, data in verification_codes.items() if current_time > data["expires_at"]]
    for key in expired_keys:
        del verification_codes[key]


async def send_email(receiver, sender="nickitaabc@gmail.com", subject="Verification", username="username", code=None):
    if code is None:
        code = confirmation_code()
    
    with open("backend/app/mailer/email_message.html", "r") as f:
        html = Template(f.read())

    with open("backend/app/mailer/email_message.txt", "r") as f:
        text = Template(f.read())

    # Форматируем смску
    # там = тут
    html = html.render(
        username=username,
        confirmation_code=code)

    text = text.render(
        username=username)

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # Преобразование в MIME-объекты и сборка письма
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    load_key_to_email()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, MAIL_KEY)
        server.send_message(msg)

    verification_codes[receiver] = {
        "code": code,
        "expires_at": time.time() + 300  # 5 минут
    }
    clean_expired_codes()
