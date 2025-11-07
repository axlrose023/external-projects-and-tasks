# region				-----External Imports-----
import fastapi
import typing
import jose
from utils.api import service as utils_service
# endregion

# region				-----Internal Imports-----
from ..... import models
from .. import schemas


# endregion

# region			  -----Supporting Variables-----
# endregion


async def authenticate_user(
        email: str,
        password: str
) -> typing.Type[models.User]:
    user = await models.User.objects.filter(
        email=email
    ).afirst()

    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    if user is None or not user.check_password(
            password
    ):
        raise credentials_exception

    if not user.email_verified:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
        )

    return user


class UserService:
    async def get_auth_tokens(
            self,
            form_data: typing.Annotated[
                fastapi.security.OAuth2PasswordRequestForm,
                fastapi.Depends(),
            ],
    ):
        user = await authenticate_user(
            form_data.username,
            form_data.password
        )

        data = {
            "subject": user.id
        }

        access_token = await utils_service.create_access_token(
            data=data
        )
        refresh_token = await utils_service.create_refresh_token(
            data=data
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(
            self,
            token_data: schemas.RefreshTokenInputSchema
    ):
        token_error = fastapi.HTTPException(
            status_code=401,
            detail="Invalid token"
        )

        try:
            payload = await utils_service.decode_token(
                token_data.refresh_token
            )

            if payload.get(
                    "token_type"
            ) != "refresh" or "subject" not in payload:
                raise token_error

            new_access_token = await utils_service.create_access_token(
                data={
                    "subject": payload.get(
                        "subject"
                    )
                }
            )

            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }

        except jose.JWTError:
            raise token_error

    async def register(
            self,
            data: schemas.RegistrationUserSchema
    ) -> typing.Type[models.User]:
        if await models.User.objects.filter(
                email=data.email
        ).aexists():
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail="Email has been already taken",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        user = models.User(
            **data.model_dump()
        )
        user.set_password(
            user.password
        )

        await user.asave()
        return user
