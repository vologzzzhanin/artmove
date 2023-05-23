from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users


class UserInSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class RestoreUserPassword(BaseModel):
    email: EmailStr


class UserUpdateSchema(BaseModel):
    full_name: str | None
    is_verified: bool | None


class UpdateUserPassword(BaseModel):
    token: str
    password: str


UserOutSchema = pydantic_model_creator(
    Users,
    name="UserOut",
    exclude=["password", "created_at", "animation", "user_images"],
)
UserDatabaseSchema = pydantic_model_creator(
    Users,
    name="User",
    exclude=["created_at", "animation", "user_images"],
)
