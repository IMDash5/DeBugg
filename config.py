import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_ALGORYTHM = os.environ.get("SECRET_ALGORYTHM")

MAIL_KEY = os.environ.get("MAIL_KEY")

GIGACHAT_API = os.environ.get("GIGACHAT_API")