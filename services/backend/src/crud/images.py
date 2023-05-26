import filetype
import io
import os
import secrets
from PIL import Image

from fastapi import HTTPException, UploadFile, status

from src.config import settings
from src.database.models import Images
from src.schemas.images import ImageOutSchema, ImageUpdateSchema
from src.schemas.users import UserOutSchema


async def upload_single_image(
    image: UploadFile,
    current_user: UserOutSchema,
) -> ImageOutSchema:
    if file_type := filetype.image_match(image.file):
        token_name = secrets.token_hex(10) + "." + file_type.extension
        path = os.path.join(settings.upload_root, token_name)
        file_content = await image.read()

        with open(path, "wb") as f:
            f.write(file_content)

        image_obj = await Images.create(
            title=image.filename,
            img=path,
            owner_id=current_user.id,
        )
        return await ImageOutSchema.from_queryset_single(Images.get(id=image_obj.id))
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"File '{image.filename}' is not an valid image",
        )


async def upload_images(
    images: list[UploadFile],
    current_user: UserOutSchema,
) -> list[ImageOutSchema]:
    image_objs = []
    for image in images:
        image_obj = await upload_single_image(image, current_user)
        image_objs.append(image_obj.id)

    return await ImageOutSchema.from_queryset(Images.filter(id__in=image_objs))


async def upload_thumbnail(
    images: list[ImageOutSchema],
    current_user: UserOutSchema,
    size: tuple[int] = (100, 100),
) -> ImageOutSchema:
    background = Image.open(images[0].img)

    for image in images[1:]:
        foreground = Image.open(image.img)
        background.paste(foreground, (0, 0), foreground)
    background.thumbnail(size)

    thumb_io = io.BytesIO()
    background.save(thumb_io, format="PNG")
    thumb_io.seek(0)
    thumbnail = UploadFile(thumb_io, size=background.size, filename="thumbnail.png")

    return await upload_single_image(thumbnail, current_user)


async def update_image(image: ImageUpdateSchema) -> ImageOutSchema | None:
    image_dict = image.dict(exclude_unset=True)
    image_id = image_dict.pop("id")

    if image_dict:
        await Images.get(id=image_id).update(**image_dict)
        return await ImageOutSchema.from_queryset_single(Images.get(id=image_id))
