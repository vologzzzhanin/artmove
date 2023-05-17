from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Compositions
from src.schemas.compositions import CompositionOutSchema
from src.schemas.token import Status


async def create_composition(animation, images) -> CompositionOutSchema:
    for order, image in enumerate(images):
        composition_dict = {
            "animation_id": animation.id,
            "image_id": image.id,
            "order": order,
        }
        await Compositions.create(**composition_dict) # TODO кривая реализация
    return await CompositionOutSchema.from_queryset(Compositions.filter(animation_id=animation.id))


async def update_composition(composition_id, composition) -> CompositionOutSchema:
    try:
        await CompositionOutSchema.from_queryset_single(Compositions.get(id=composition_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Composition {composition_id} not found")

    await Compositions.filter(id=composition_id).update(**composition.dict(exclude_unset=True))
    return await CompositionOutSchema.from_queryset_single(Compositions.get(id=composition_id))


async def delete_composition(composition_id) -> Status:
    try:
        await CompositionOutSchema.from_queryset_single(Compositions.get(id=composition_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Composition {composition_id} not found")

    deleted_count = await Compositions.filter(id=composition_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Composition {composition_id} not found")
    return Status(message=f"Deleted composition {composition_id}")
