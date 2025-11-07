# region				-----External Imports-----
import pydantic
import pydantic_settings

# endregion


class APISettings(pydantic_settings.BaseSettings):
    JWT_SECRET_KEY: str = pydantic.Field("foo", validation_alias="SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 60  # ? minutes | one hour
    REFRESH_TOKEN_EXPIRE: int = 1  # ? days | one day


API_SETTINGS = APISettings()
