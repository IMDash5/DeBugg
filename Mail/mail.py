import smtplib, os, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Template


def load_key_to_email():
    load_dotenv()  # Загружает переменные из .env
    # load_dotenv(dotenv_path="/полный/путь/к/файлу/.env")
    print("❌ Not found .env!") if os.getenv("KEY") is None else print("✅ Key uploaded")


def confirmation_code():
    confirmation_code = str(secrets.randbelow(10 ** 6)).zfill(6)
    print(confirmation_code)
    return confirmation_code


def send_email(sender, receiver, subject, username, code):
    with open("email_message.html", "r") as f:
        html = Template(f.read())

    with open("email_message.txt", "r") as f:
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
        server.login(sender, os.getenv("KEY"))
        server.send_message(msg)
        print("✅ Письмо успешно отправлено!")


send_email(
    sender="nickitaabc@gmail.com",
    receiver="nick.evtenko@gmail.com",
    subject="BLAAAAAAAAAAA",
    username="XUI BLA",
    code=confirmation_code()
)
