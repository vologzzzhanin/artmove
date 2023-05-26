from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Animations
from src.schemas.compositions import CompositionUpdateSchema


class AnimationInSchema(BaseModel):
    title: str


AnimationOutSchema = pydantic_model_creator(
    Animations,
    name="AnimationOut",
    include=[
        "id", "title", "background",
        "modified_at", "author_id",
        "thumbnail_id", "thumbnail",
        "composition",
    ],
    exclude=[
        "composition.image.owner",
        "thumbnail.owner",
        "thumbnail.composition",
    ],
)


class AnimationUpdateSchema(BaseModel):
    """Анимация"""
    title: str | None
    background: str | None
    composition: list[CompositionUpdateSchema] | None
