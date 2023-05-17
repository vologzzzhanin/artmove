from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import HTTPNotFoundError

import src.crud.users as crud
from src.auth.jwthandler import (
    create_token,
    get_current_user,
    get_verified_user,
)
from src.auth.users import validate_user
from src.auth.emails import send_confirmation_email
from src.config import settings
from src.schemas.token import Status, VerificationToken
from src.schemas.users import (
    UpdateUserPassword,
    UserInSchema,
    UserOutSchema,
    UserUpdateSchema,
)

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    new_user = await crud.create_user(user)
    confirmation_token = create_token(
        data={"sub": str(new_user.id)},
        expires_in=settings.confirmation_token_expires_in,
    )
    await send_confirmation_email(user, confirmation_token)

    return new_user


@router.post("/email_confirm")
async def verify_user(data: VerificationToken) -> UserOutSchema:
    user = await get_verified_user(data.token)
    return await crud.verify_user(user.id)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):  # noqa TODO разобраться с этим дерьмом https://www.youtube.com/watch?v=lfT6a9VqyLM
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token(
        data={"sub": user.email},
        expires_in=settings.access_token_expires_in,
    )
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    return response


@router.get(
    "/users/whoami", response_model=UserOutSchema, dependencies=[Depends(get_current_user)]
)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)) -> UserOutSchema:
    return current_user


@router.post(
    "/update_password",
    response_model=UserOutSchema,
    dependencies=[Depends(get_current_user)]
)
async def update_password(
    user_password: UpdateUserPassword,
    current_user: UserOutSchema = Depends(get_current_user),
) -> UserOutSchema:
    return await crud.update_user_password(user_password, current_user)


@router.patch(
    "/user/{user_id}",
    response_model=UserOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def update_user(  # TODO на удаление
    user_id: int,
    user_data: UserUpdateSchema,
    current_user: UserOutSchema = Depends(get_current_user),
) -> UserOutSchema:
    return await crud.update_user(user_id, user_data, current_user)


@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    return await crud.delete_user(user_id, current_user)
