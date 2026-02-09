import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Flask Security
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email (Gmail SMTP)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # Encryption Key
    FIELD_ENCRYPTION_KEY = os.getenv("FIELD_ENCRYPTION_KEY")

    # MFA
    MFA_CODE_EXPIRATION = 300  # seconds
