# region				-----External Imports-----
import typing
# endregion

# region				-----Internal Imports-----
from .posts_creation_service import AddPostService
from .posts_retrieval_service import GetPostService
from .posts_deletion_service import DeletePostService
# endregion

# region			  -----Supporting Variables-----
# endregion


class PostFacade:
    def __init__(
            self
    ):
        self.add_service = AddPostService()
        self.get_service = GetPostService()
        self.delete_service = DeletePostService()

    async def create_post(
            self,
            text: str,
            user: typing.Any
    ) -> int:
        return await self.add_service.create_post(
            text,
            user
        )

    async def get_posts(
            self,
            user: typing.Any
    ):
        return await self.get_service.get_posts(
            user
        )

    async def delete_post(
            self,
            post_id: int,
            user: typing.Any
    ):
        return await self.delete_service.delete_post(
            post_id,
            user
        )
