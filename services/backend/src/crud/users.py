from fastapi import HTTPException, status
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
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


async def update_user_password(user, current_user) -> Status:
    current_user.password = pwd_context.encrypt(user.password)
    current_user.save()

    return Status(message="You have successfully updated password")


async def update_user(user_id, user, current_user) -> UserOutSchema:
    db_user = await get_user(user_id)

    if db_user.id == current_user.id or current_user.is_superuser:
        await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
        return await UserOutSchema.from_queryset_single(Users.get(id=user_id))

    raise HTTPException(status_code=403, detail="Not authorized to update")


async def delete_user(user_id, current_user) -> Status:
    if current_user.is_superuser:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail="Not authorized to delete")
