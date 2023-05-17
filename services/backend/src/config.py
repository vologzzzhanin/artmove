from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    mail_username: EmailStr
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str
    mail_from_name: str
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool
    validate_certs: bool

    secret_key: str
    algorithm: str
    access_token_expires_in: int
    confirmation_token_expires_in: int

    database_url: str
    frontend_url: str
    upload_root: str

    service_name: str


settings = Settings(_env_file=".env.local", _env_file_encoding="utf-8")
