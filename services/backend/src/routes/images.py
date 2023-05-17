from fastapi import APIRouter, Depends, UploadFile

import src.crud.images as crud
from src.auth.jwthandler import get_current_user
from src.schemas.images import ImageOutSchema
from src.schemas.users import UserOutSchema


router = APIRouter(tags=["Images"], dependencies=[Depends(get_current_user)])


@router.post("/images")
async def upload_images(
    images: list[UploadFile],
    current_user: UserOutSchema = Depends(get_current_user),
) -> list[ImageOutSchema]:
    return await crud.upload_images(images, current_user)
