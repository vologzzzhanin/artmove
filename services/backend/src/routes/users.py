from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

import src.crud.users as crud
from src.auth.jwthandler import (
    create_token,
    get_authenticated_user,
    get_current_user,
)
from src.auth.users import validate_user
from src.auth.emails import send_confirmation_email, send_recovery_email
from src.config import settings
from src.schemas.token import Status, VerificationToken
from src.schemas.users import (
    RestoreUserPassword,
    UpdateUserPassword,
    UserInSchema,
    UserOutSchema,
    UserUpdateSchema,
)

router = APIRouter(tags=["Users"])


@router.post("/register")
async def create_user(user: UserInSchema) -> JSONResponse:
    new_user = await crud.create_user(user)
    confirmation_token = create_token(
        user=new_user,
        expires_in=settings.confirmation_token_expires_in,
    )
    await send_confirmation_email(user, confirmation_token)

    content = {"message": "A confirmation email has been sent"}
    return JSONResponse(content=content)


@router.post("/email_confirm")
async def verify_user(data: VerificationToken) -> JSONResponse:
    user, expired = await get_authenticated_user(data.token)

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has already been verified",
        )

    if expired:
        new_confirmation_token = create_token(
            user=user,
            expires_in=settings.confirmation_token_expires_in,
        )
        await send_confirmation_email(user, new_confirmation_token)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This email verification token has expired. A new token has been sent to your email",
        )

    data = UserUpdateSchema(is_verified=True)
    await crud.update_user(user.id, data)

    return Status(message="You have successfully verify account")


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:  # noqa TODO разобраться с этим дерьмом https://www.youtube.com/watch?v=lfT6a9VqyLM
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token(
        user=user,
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


@router.get("/users/whoami")
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)) -> UserOutSchema:
    return current_user


@router.post("/restore_password")
async def restore_password(user: RestoreUserPassword) -> JSONResponse:
    db_user = await crud.get_user_by_email(email=user.email)

    recovery_token = create_token(
        user=db_user,
        expires_in=settings.recovery_token_expires_in,
    )
    await send_recovery_email(user, recovery_token)

    content = {"message": "A password reset link has been sent to your email"}
    return JSONResponse(content=content)


@router.post("/update_password")
async def update_password(data: UpdateUserPassword) -> JSONResponse:
    user, expired = await get_authenticated_user(data.token)

    if expired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This password reset link has expired",
        )

    return await crud.update_user_password(user.id, data)
