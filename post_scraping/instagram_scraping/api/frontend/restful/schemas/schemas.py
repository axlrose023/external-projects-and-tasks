# region				-----External Imports-----
from pydantic import BaseModel, Field, field_validator
import re
# endregion

class PostSchema(
    BaseModel
):
    description: str
    likes: int
    comments: int
    hashtag_present: bool
    hashtag_count: int

    @field_validator(
        "description"
    )
    def clean_description(
            cls,
            value: str
    ) -> str:
        value = re.sub(
            r"\s+",
            " ",
            value
        ).strip()
        value = re.sub(
            r"▃+",
            "",
            value
        ).strip()
        return value


class ScrapeRequestSchema(
    BaseModel
):
    target_username: str
    hashtag: str
    login_username: str
    login_password: str
    count: int = 10


class ScrapedPostsResponseSchema(
    BaseModel
):
    posts: list
