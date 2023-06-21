
from src.crud.images import update_image
from src.database.models import Compositions
from src.schemas.compositions import (
    CompositionInSchema,
    CompositionOutSchema,
    CompositionUpdateSchema,
)
from src.schemas.images import ImageOutSchema


async def create_composition(
    animation_id: int,
    images: list[ImageOutSchema],
) -> list[CompositionOutSchema]:
    for order, image in enumerate(images):
        element = CompositionInSchema(
            animation_id=animation_id,
            image_id=image.id,
            order=order,
        )
        await Compositions.create(**element.dict(exclude_unset=True))
    return await CompositionOutSchema.from_queryset(
        Compositions.filter(animation_id=animation_id)
    )


async def update_composition(
    animation_id: int,
    composition: list[CompositionUpdateSchema],
) -> list[CompositionOutSchema]:
    await (
        Compositions
        .filter(animation_id=animation_id)
        .exclude(id__in=[c.id for c in composition])
        .delete()
    )
    for element in composition:
        defaults = element.dict(exclude={"id", "image"})
        await Compositions.update_or_create(
            defaults,
            id=element.id,
            image_id=element.image.id,
        )

        await update_image(element.image)
    return await CompositionOutSchema.from_queryset(
        Compositions.filter(animation_id=animation_id)
    )
