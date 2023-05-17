from pydantic import BaseModel


class VerificationToken(BaseModel):
    token: str


class TokenData(BaseModel):
    email: str | None = None


class Status(BaseModel):
    message: str
