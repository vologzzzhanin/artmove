from pydantic import BaseModel, EmailStr, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users


class UserInSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UpdateUserPassword(BaseModel):
    password: SecretStr


UserOutSchema = pydantic_model_creator(
    Users,
    name="UserOut",
    exclude=["password", "created_at", "modified_at", "animation", "user_images"],
)
UserUpdateSchema = pydantic_model_creator(
    Users, name="UserUpdate", include=["email", "full_name", "is_superuser"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)
