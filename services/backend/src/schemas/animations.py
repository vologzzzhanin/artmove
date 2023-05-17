from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Animations


class AnimationInSchema(BaseModel):
    title: str


AnimationOutSchema = pydantic_model_creator(
    Animations,
    name="AnimationOut",
    include=[
        "id", "title", "background",
        "modified_at", "author_id",
        "thumbnail_id", "thumbnail",
        "compositions",
    ],
    exclude=[
        "compositions.image.owner",
        "thumbnail.owner",
        "thumbnail.image_compositions",
    ],
)


class Image(BaseModel):
    """Изображение"""
    id: int
    title: str | None


class Options(BaseModel):
    """Опции композиции"""
    opacity: float | None
    visible: bool | None = True


class Composition(BaseModel):
    """Композиция"""
    id: int
    image: Image | None
    order: int | None
    options: Options | None


class AnimationUpdate(BaseModel):
    """Анимация"""
    title: str | None
    background: str | None
    compositions: list[Composition] | None
