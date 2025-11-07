# region				-----External Imports-----
import typing
import fastapi
from fastapi import security as fastapi_security
from fastapi_restful.cbv import cbv
from utils.api import service as utils_api_service
from utils.api import views as utils_api_views
# endregion

# region				-----Internal Imports-----
from .. import schemas
from .. import service
from ..... import models
# endregion

# region			  -----Supporting Variables-----
user_service = service.UserService()
# endregion

user_router = fastapi.APIRouter(
    prefix="/user",
    tags=["user"]
)


@user_router.post(
    "/token",
    response_model=schemas.AccesTokenResponseSchema
)
async def token(
        form_data: typing.Annotated[
            fastapi_security.OAuth2PasswordRequestForm,
            fastapi.Depends(),
        ]
):
    return await user_service.get_auth_tokens(
        form_data=form_data
    )


@user_router.post(
    path="/token/refresh",
    response_model=schemas.RefreshTokenResponseSchema
)
async def refresh_token(
        token_data: schemas.RefreshTokenInputSchema
):
    return await user_service.refresh_token(
        token_data=token_data
    )


@user_router.post(
    path="/",
    response_model=schemas.ReadUserSchema,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def register(
        user_data: schemas.RegistrationUserSchema
):
    return await user_service.register(
        data=user_data
    )


@cbv(
    user_router
)
class UsersView(
    utils_api_views.APIViewMixin
):
    queryset = models.User.objects

    user: typing.Type[models.User] = fastapi.Depends(
        utils_api_service.get_current_user
    )

    @user_router.get(
        path="/",
        response_model=schemas.ReadUserSchema
    )
    async def get_current_user(
            self
    ):
        return await self.get_object(
            self.user.id
        )
