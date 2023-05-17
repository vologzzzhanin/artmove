from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from src.database.models import Users
from src.schemas.users import UserDatabaseSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(email: str):
    return await UserDatabaseSchema.from_queryset_single(Users.get(email=email))


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    validation_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    try:
        db_user = await get_user(user.username)
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
