# region				-----External Imports-----
import typing
import fastapi
import fastapi_pagination
from django.db import models as django_models
from django.utils import timezone
from django.conf import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from user import models as user_models

# endregion

# region				-----Internal Imports-----
from .. import schemas

# endregion

# region			  -----Supporting Variables-----
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl="/api/frontend/user/token",
    auto_error=False,
)

T = typing.TypeVar(
    "T",
    bound=django_models.Model
)
# endregion


async def get_current_user(
        token: typing.Optional[str] = fastapi.Depends(
            oauth2_scheme
        ),
        raise_error: bool = True,
) -> typing.Type[user_models.User]:
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    if not token:
        if raise_error:
            raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.API_SETTINGS.JWT_SECRET_KEY,
            algorithms=[settings.API_SETTINGS.JWT_ALGORITHM],
        )
        subject: int = payload.get(
            "subject"
        )

        if subject is None:
            raise credentials_exception

        if payload.get(
                "token_type"
        ) != "access":
            raise credentials_exception

        token_data = schemas.TokenData(
            id=subject
        )
    except JWTError:
        raise credentials_exception

    user = await user_models.User.objects.filter(
        id=token_data.id
    ).afirst()

    if user is None:
        raise credentials_exception

    return user


async def create_access_token(
        data: dict,
        expire_delta: typing.Union[timezone.timedelta, None] = None,
) -> str:
    to_encode = data.copy()

    if expire_delta:
        expire = timezone.now() + expire_delta
    else:
        expire = timezone.now() + timezone.timedelta(
            minutes=settings.API_SETTINGS.ACCESS_TOKEN_EXPIRE
        )

    to_encode.update(
        {
            "exp": expire
        }
    )
    to_encode.update(
        {
            "token_type": "access"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.API_SETTINGS.JWT_SECRET_KEY,
        algorithm=settings.API_SETTINGS.JWT_ALGORITHM,
    )

    return encoded_jwt


async def create_refresh_token(
        data: dict,
        expire_delta: typing.Union[timezone.timedelta, None] = None,
) -> str:
    to_encode = data.copy()

    if expire_delta is not None:
        expire = timezone.now() + expire_delta
    else:
        expire = timezone.now() + timezone.timedelta(
            days=settings.API_SETTINGS.REFRESH_TOKEN_EXPIRE
        )

    to_encode.update(
        {
            "exp": expire
        }
    )
    to_encode.update(
        {
            "token_type": "refresh"
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.API_SETTINGS.JWT_SECRET_KEY,
        algorithm=settings.API_SETTINGS.JWT_ALGORITHM,
    )

    return encoded_jwt


async def decode_token(
        token: str,
):
    try:
        payload = jwt.decode(
            token,
            settings.API_SETTINGS.JWT_SECRET_KEY,
            algorithms=[settings.API_SETTINGS.JWT_ALGORITHM],
        )

        return payload
    except JWTError:
        return {}
