from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

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


async def send_confirmation_email(user: UserOutSchema, token: str):
    """Отправка email для подтверждения регистрации пользователя"""
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
                Please click and verify your account
            </a>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=settings.service_name + " account confirmation",
        recipients=[user.email],
        body=template,
        subtype=MessageType.html,
    )
    mail_service = FastMail(config)
    await mail_service.send_message(message)
