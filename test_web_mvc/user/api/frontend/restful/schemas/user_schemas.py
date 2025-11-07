# region				-----External Imports-----
import pydantic
import typing
import string
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion


class AccesTokenResponseSchema(
    pydantic.BaseModel
):
    access_token: str
    refresh_token: str
    token_type: str

    model_config = pydantic.ConfigDict(
        json_schema_extra={
            "examples": [{
                "token_type": "bearer"
            }]
        }
    )


class RefreshTokenInputSchema(
    pydantic.BaseModel
):
    refresh_token: str
    token_type: str

    model_config = pydantic.ConfigDict(
        json_schema_extra={
            "examples": [{
                "token_type": "bearer"
            }]
        }
    )


class RefreshTokenResponseSchema(
    pydantic.BaseModel
):
    access_token: str
    token_type: str

    model_config = pydantic.ConfigDict(
        json_schema_extra={
            "examples": [{
                "token_type": "bearer"
            }]
        }
    )


class BaseUserSchema(
    pydantic.BaseModel
):
    email: pydantic.EmailStr

    model_config = pydantic.ConfigDict(
        from_attributes=True
    )


class ReadUserSchema(
    BaseUserSchema
):
    id: int
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]
    username: typing.Optional[str]
    email_verified: bool
    registered_using_social_media: bool


class BaseUserPasswordSchema(
    pydantic.BaseModel
):
    password: str
    confirm_password: str = pydantic.Field(
        ...,
        exclude=True
    )

    @pydantic.model_validator(
        mode="after"
    )
    def passwords_match(
            self
    ):
        password = self.password
        confirm_password = self.confirm_password

        if len(
                password
        ) < 8 or len(
            confirm_password
        ) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        if not any(
                char.isupper() for char in password
        ):
            raise ValueError(
                "Password must contain at least one upper case symbol"
            )

        if not any(
                char.islower() for char in password
        ):
            raise ValueError(
                "Password must contain at least one lower case symbol"
            )

        if not any(
                char in string.punctuation for char in password
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )

        if password != confirm_password:
            raise ValueError(
                "Passwords don't match"
            )

        return self


class RegistrationUserSchema(
    BaseUserPasswordSchema,
    BaseUserSchema
):
    ...
