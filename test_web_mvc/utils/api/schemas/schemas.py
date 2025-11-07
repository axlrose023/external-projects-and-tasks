# region				-----External Imports-----
import typing
import pydantic

# endregion


class TokenData(pydantic.BaseModel):
    id: typing.Optional[int] = None
