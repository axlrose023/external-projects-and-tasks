# region				-----External Imports-----
import typing
import fastapi
# endregion

# region				-----Internal Imports-----
from ..... import models
# endregion


class AddPostService:
    async def create_post(
            self,
            text: str,
            user: typing.Any
    ) -> int:
        self._validate_payload_size(
            text
        )
        new_post = await models.Post.objects.acreate(
            text=text,
            user=user
        )
        return new_post.id

    def _validate_payload_size(
            self,
            text: str
    ) -> None:
        if len(
                text.encode(
                    "utf-8"
                )
        ) > 1024 * 1024:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail="Payload exceeds the maximum allowed size of 1 MB"
            )
