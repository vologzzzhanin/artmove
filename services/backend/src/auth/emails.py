from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from src.config import settings
from src.schemas.users import UserOutSchema

config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)


async def send_confirmation_email(user: UserOutSchema, token: str) -> None:
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div style="display:flex; align-items: center; flex-direction: column">
            <h3>Account confirmation</h3>
            <br>
            <a style="display:flex; margin-top: 1rem; padding: 1rem; border-radius: 0.5rem;
            font-size:1rem; background: #0275d8; color:white"
            href="{settings.frontend_url}/email_confirm/?token={token}">
                Please click to verify your account
            </a>
        </div>
    </body>
    </html>
    """
    subject = settings.service_name + " account confirmation"

    await send_email(email=user.email, template=template, subject=subject)


async def send_recovery_email(user: UserOutSchema, token: str) -> None:
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div style="display:flex; align-items: center; flex-direction: column">
            <h3>Password recovery</h3>
            <br>
            <a style="display:flex; margin-top: 1rem; padding: 1rem; border-radius: 0.5rem;
            font-size:1rem; background: #0275d8; color:white"
            href="{settings.frontend_url}/update_password/?token={token}">
                Please click to update your password
            </a>
        </div>
    </body>
    </html>
    """
    subject = settings.service_name + " password recovery"

    await send_email(email=user.email, template=template, subject=subject)


async def send_email(email: EmailStr, template: str, subject: str) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=template,
        subtype=MessageType.html,
    )
    mail_service = FastMail(config)
    await mail_service.send_message(message)
