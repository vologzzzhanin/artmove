from fastapi import HTTPException, Depends, status
from fastapi.param_functions import Form
from passlib.context import CryptContext
from pydantic import EmailStr
from tortoise.exceptions import DoesNotExist

from src.database.models import Users
from src.schemas.users import UserDatabaseSchema


class LoginRequestForm:
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        email: EmailStr = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def validate_user(
    user: LoginRequestForm = Depends(),
) -> UserDatabaseSchema:
    validation_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    try:
        db_user = await UserDatabaseSchema.from_queryset_single(Users.get(email=user.email))
    except DoesNotExist:
        raise validation_exception

    if not verify_password(user.password, db_user.password):
        raise validation_exception

    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your email was not verified",
        )

    return db_user
