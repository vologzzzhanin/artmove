from fastapi import HTTPException, UploadFile, status
from tortoise import transactions
from tortoise.exceptions import DoesNotExist

from src.crud.compositions import create_composition, update_composition
from src.crud.images import upload_images, upload_thumbnail
from src.database.models import Animations
from src.schemas.animations import (
    AnimationInSchema,
    AnimationOutSchema,
    AnimationUpdateSchema,
)
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


async def get_animations(current_user: UserOutSchema) -> list[AnimationOutSchema]:
    return await AnimationOutSchema.from_queryset(
        Animations
        .filter(author_id=current_user.id)
        .order_by("-modified_at")
    )


async def get_animation(animation_id: int, current_user: UserOutSchema) -> AnimationOutSchema:
    db_animation = await AnimationOutSchema.from_queryset_single(Animations.get(id=animation_id))

    if db_animation.author_id == current_user.id:
        return db_animation

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to get animation",
    )


@transactions.atomic()
async def create_animation(
    animation: AnimationInSchema,
    images: list[UploadFile],
    current_user: UserOutSchema,
) -> AnimationOutSchema:
    # First of all create animation obj
    animation_dict = animation.dict(exclude_unset=True)
    animation_dict["author_id"] = current_user.id
    db_animation = await Animations.create(**animation_dict)
    # Secondary upload user images
    db_images = await upload_images(images, current_user)
    # Then make thumbnail
    db_thumbnail = await upload_thumbnail(db_images, current_user)
    db_animation.thumbnail = db_thumbnail
    await db_animation.save()
    # Finally map animation with images into composition
    await create_composition(db_animation.id, db_images)
    return await AnimationOutSchema.from_queryset_single(Animations.get(id=db_animation.id))


@transactions.atomic()
async def update_animation(
    animation_id: int,
    animation: AnimationUpdateSchema,
    current_user: UserOutSchema,
) -> AnimationOutSchema:
    try:
        db_animation = await AnimationOutSchema.from_queryset_single(Animations.get(id=animation_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Animation {animation_id} not found")

    animation_dict = animation.dict(exclude_unset=True)
    if db_animation.author_id == current_user.id:
        if _ := animation_dict.pop("composition", None):
            await update_composition(animation_id, animation.composition)

        await Animations.filter(id=animation_id).update(**animation_dict)
        return await AnimationOutSchema.from_queryset_single(Animations.get(id=animation_id))

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to update",
    )


async def delete_animation(animation_id: int, current_user: UserOutSchema) -> Status:
    try:
        db_animation = await AnimationOutSchema.from_queryset_single(Animations.get(id=animation_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Animation {animation_id} not found",
        )

    if db_animation.author_id == current_user.id:
        deleted_count = await Animations.filter(id=animation_id).delete()
        if not deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Animation {animation_id} not found",
            )
        return Status(message=f"Deleted animation {animation_id}")

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to delete",
    )
