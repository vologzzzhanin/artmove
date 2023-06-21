from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import EmailStr
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import (
    UpdateUserPassword,
    UserInSchema,
    UserOutSchema,
    UserUpdateSchema,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserInSchema) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sorry, user with this email already exists",
        )

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def verify_user(user_id: int) -> UserOutSchema:
    await Users.filter(id=user_id).update(is_verified=True)
    return await UserOutSchema.from_queryset_single(Users.get(id=user_id))


async def get_user(user_id: int) -> UserOutSchema:
    try:
        return await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )


async def get_user_by_email(email: EmailStr) -> UserOutSchema:
    try:
        return await UserOutSchema.from_queryset_single(Users.get(email=email))
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )


async def update_user(user_id: int, data: UserUpdateSchema) -> UserOutSchema:
    await Users.filter(id=user_id).update(**data.dict(exclude_unset=True))
    return await UserOutSchema.from_queryset_single(Users.get(id=user_id))


async def update_user_password(user_id: int, data: UpdateUserPassword) -> Status:
    db_user = await Users.get(id=user_id)
    db_user.password = pwd_context.encrypt(data.password)
    await db_user.save()

    return Status(message="You have successfully update password")
