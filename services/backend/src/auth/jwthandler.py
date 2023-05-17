from calendar import timegm
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from src.auth.emails import send_confirmation_email
from src.config import settings
from src.crud.users import get_user
from src.database.models import Users
from src.schemas.token import TokenData
from src.schemas.users import UserOutSchema


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


security = OAuth2PasswordBearerCookie(token_url="/login")


def create_token(data: dict, expires_in: int | None = None) -> str:
    to_encode = data.copy()

    if expires_in:
        expires_delta = timedelta(minutes=expires_in)
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return jsonable_encoder(encoded_jwt)


async def get_current_user(token: str = Depends(security)) -> UserOutSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    try:
        user = await UserOutSchema.from_queryset_single(
            Users.get(email=token_data.email)
        )
    except DoesNotExist:
        raise credentials_exception

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your email was not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_verified_user(token: str) -> UserOutSchema:
    email_verification_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify user email",
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False},
        )
        try:
            user_id = int(payload.get("sub"))
            exp = int(payload.get("exp"))
        except ValueError:
            raise email_verification_exception

        if user_id is None:
            raise email_verification_exception

        user = await get_user(user_id=user_id)
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has already been verified",
            )

        now = timegm(datetime.utcnow().utctimetuple())

        if exp < now:
            new_confirmation_token = create_token(
                data={"sub": str(user.id)},
                expires_in=settings.confirmation_token_expires_in,
            )
            await send_confirmation_email(user, new_confirmation_token)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This email verification token has expired. A new token has been sent to your email",
            )
    except JWTError:
        raise email_verification_exception

    return user
