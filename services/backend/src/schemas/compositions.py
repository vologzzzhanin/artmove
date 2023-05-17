from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Compositions


CompositionOutSchema = pydantic_model_creator(
    Compositions, name="CompositionOut", exclude_readonly=True
)
