from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Images


ImageOutSchema = pydantic_model_creator(
    Images, name="ImageOut", exclude=["owner", "image_compositions"]
)


class ImageUpdateSchema(BaseModel):
    id: int
    title: str | None
