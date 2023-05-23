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


class AuthorizationEmail:
    def __init__(
        self,
        *,
        header: str,
        route: str,
        link_text: str,
        config: ConnectionConfig = config,
    ) -> None:
        self.header = header
        self.route = route
        self.link_text = link_text
        self.service=FastMail(config)

    def body(self, token: str) -> str:
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <div style="display:flex; align-items: center; flex-direction: column">
                    <h3>{self.header}</h3>
                    <br>
                    <a style="display:flex; margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size:1rem; background: #0275d8; color:white" href="{settings.frontend_url}/{self.route}/?token={token}">{self.link_text}</a>
                </div>
            </body>
            </html>"""

    @property
    def subject(self) -> str:
        return f"{settings.service_name} {self.header.lower()}"

    async def send(self, user: UserOutSchema, token: str) -> None:
        message = MessageSchema(
            recipients=[user.email],
            subject=self.subject,
            body=self.body(token),
            subtype=MessageType.html,
        )
        await self.service.send_message(message)
