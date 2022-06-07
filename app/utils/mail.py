from datetime import datetime, timedelta
from typing import Optional
import smtplib
import ssl


from jose import jwt

from app.config import settings
from app.models.codes import Code


def send_email(email_to, message):

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "nvanson.2201@gmail.com"
    receiver_email = email_to
    password = "pzkndtxfygyjnrcu"
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    message = f"""\
    Subject: Hi there

    This message is sent from fastapi_blog.

    Your link to reset password: {link}
    """
    send_email(email_to=email_to, message=message)


def send_new_account_email(email_to: str, signup_code: Code) -> None:
    message = f"""\
    Subject: Hi there

    This message is sent from fastapi_blog.

    Your code: {signup_code}
    """
    send_email(email_to=email_to, message=message)


def generate_password_reset_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    encoded_jwt = jwt.encode(
        {"exp": expire, "sub": str(email)},
        settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])

        return decoded_token["sub"]
    except jwt.JWTError as e:
        print(e)
        return None
