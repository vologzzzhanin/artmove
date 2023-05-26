from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.animations as crud
from src.auth.jwthandler import get_current_user
from src.schemas.animations import (
    AnimationInSchema,
    AnimationOutSchema,
    AnimationUpdateSchema,
)
from src.schemas.token import Status
from src.schemas.users import UserOutSchema

router = APIRouter(tags=["Animations"], dependencies=[Depends(get_current_user)])


@router.get("/animations")
async def get_animations(
    current_user: UserOutSchema = Depends(get_current_user)
) -> list[AnimationOutSchema]:
    return await crud.get_animations(current_user)


@router.get("/animation/{animation_id}")
async def get_animation(
    animation_id: int,
    current_user: UserOutSchema = Depends(get_current_user),
) -> AnimationOutSchema:
    try:
        return await crud.get_animation(animation_id, current_user)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Animation does not exist",
        )


def checker(animation: str = Form(...)):
    try:
        model = AnimationInSchema.parse_raw(animation)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=jsonable_encoder(e.errors()),
        )
    return model


@router.post("/animations")
async def create_animation(
    animation: AnimationInSchema = Depends(checker),
    images: list[UploadFile] = File(...),
    current_user: UserOutSchema = Depends(get_current_user),
) -> AnimationOutSchema:
    return await crud.create_animation(animation, images, current_user)


@router.patch(
    "/animation/{animation_id}",
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_animation(
    animation_id: int,
    animation: AnimationUpdateSchema,
    current_user: UserOutSchema = Depends(get_current_user),
) -> AnimationOutSchema:
    return await crud.update_animation(animation_id, animation, current_user)


@router.delete(
    "/animation/{animation_id}",
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_animation(
    animation_id: int,
    current_user: UserOutSchema = Depends(get_current_user),
) -> Status:
    return await crud.delete_animation(animation_id, current_user)
