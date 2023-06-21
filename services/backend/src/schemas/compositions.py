from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Compositions
from src.schemas.images import ImageUpdateSchema


CompositionOutSchema = pydantic_model_creator(
    Compositions, name="CompositionOut", exclude_readonly=True
)


class Options(BaseModel):
    """Composition options schema"""
    opacity: float | None = 1
    visible: bool | None = True


class CompositionInSchema(BaseModel):
    animation_id: int
    image_id: int
    order: int
    options: Options | None


class CompositionUpdateSchema(BaseModel):
    id: int
    image: ImageUpdateSchema
    order: int
    options: Options
