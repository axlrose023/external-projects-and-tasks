# region				-----External Imports-----
import pydantic
import typing
import datetime


# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion


class AddPostRequest(
    pydantic.BaseModel
):
    text: str

    model_config = pydantic.ConfigDict(
        extra="ignore"
    )


class AddPostResponse(
    pydantic.BaseModel
):
    postID: int

    model_config = pydantic.ConfigDict(
        extra="ignore"
    )


class PostSchema(
    pydantic.BaseModel
):
    id: int
    text: str
    created_at: datetime.datetime

    model_config = pydantic.ConfigDict(
        from_attributes=True
    )


class GetPostResponse(
    pydantic.BaseModel
):
    posts: typing.List[PostSchema]

    model_config = pydantic.ConfigDict(
        extra="ignore"
    )


class DeletePostResponse(
    pydantic.BaseModel
):
    detail: str

    model_config = pydantic.ConfigDict(
        extra="ignore"
    )
