from calendar import timegm
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt

from src.config import settings
from src.crud.users import get_user_by_email
from src.schemas.token import TokenData
from src.schemas.users import UserOutSchema


class OAuth2PasswordBearerCookie(OAuth2):
    """
    Unlike the standard OAuth2PasswordBearer,
    it takes the authorization data not from Headers, but from the Cookies
    """
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
        authorization = request.cookies.get("Authorization")
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


def create_token(user: UserOutSchema, expires_in: int | None = None) -> str:
    data = {"sub": user.email}
    to_encode = data.copy()

    if expires_in:
        expires_delta = timedelta(minutes=expires_in)
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return jsonable_encoder(encoded_jwt)


class JWTHandler:
    """JSON Web Token Handler"""
    def __init__(
        self,
        *,
        exception: HTTPException = None,
        verify_exp: bool = True,
    ) -> None:
        self.exception = exception or HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.verify_exp = verify_exp

    async def handle_token(self, token: str) -> tuple[UserOutSchema, bool | None]:
        """
        Token processing

        Return the user and the optional expiration check flag
        (needed for verification or when changing the user's password)

        Causes an exception if the user was changed after the token was issued
        """
        try:
            self.payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
                options={"verify_exp": self.verify_exp},
            )
            try:
                email: str = self.payload.get("sub")
                if email is None:
                    raise self.exception

                token_data = TokenData(email=email)
                user = await get_user_by_email(email=token_data.email)

                if self.user_has_been_modified(user):
                    raise self.exception

                return user, None if self.verify_exp else self.expired
            except ValueError:
                raise self.exception
        except JWTError:
            raise self.exception

    @property
    def expired(self) -> bool:
        try:
            exp = int(self.payload.get("exp"))
        except ValueError:
            raise self.exception

        return exp < timegm(datetime.utcnow().utctimetuple())

    def user_has_been_modified(self, user: UserOutSchema) -> bool:
        iat = int(self.payload.get("iat"))

        return iat < timegm(user.modified_at.utctimetuple())


async def get_current_user(token: str = Depends(security)) -> UserOutSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    jwt_handler = JWTHandler(exception=credentials_exception)

    user, _ = await jwt_handler.handle_token(token)

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your email was not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_authenticated_user(token: str) -> UserOutSchema:
    email_authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate user by this email",
    )
    jwt_handler = JWTHandler(
        exception=email_authentication_exception,
        verify_exp=False,
    )

    return await jwt_handler.handle_token(token)
