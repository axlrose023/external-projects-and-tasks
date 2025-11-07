# region				-----External Imports-----
from fastapi_restful.cbv import cbv
import typing
import fastapi
from utils.api import service as utils_api_service
# endregion

# region				-----Internal Imports-----
from .. import schemas
from .. import service
# endregion

# region			  -----Supporting Variables-----
post_router = fastapi.APIRouter(
    prefix="/posts",
    tags=["posts"]
)
# endregion


@cbv(
    post_router
)
class PostView:
    posts_service: typing.ClassVar[service.PostFacade] = service.PostFacade()
    current_user: typing.Any = fastapi.Depends(
        utils_api_service.get_current_user
    )

    @post_router.post(
        "/",
        response_model=schemas.AddPostResponse
    )
    async def add_post(
            self,
            post: schemas.AddPostRequest
    ):
        post_id = await self.posts_service.create_post(
            text=post.text,
            user=self.current_user
        )
        return schemas.AddPostResponse(
            postID=post_id
        )

    @post_router.get(
        "/",
        response_model=schemas.GetPostResponse
    )
    async def get_posts(
            self
    ):
        posts = await self.posts_service.get_posts(
            user=self.current_user
        )
        return schemas.GetPostResponse(
            posts=posts or []
        )

    @post_router.delete(
        "/{post_id}",
        response_model=schemas.DeletePostResponse
    )
    async def delete_post(
            self,
            post_id: int
    ):
        await self.posts_service.delete_post(
            post_id=post_id,
            user=self.current_user
        )
        return schemas.DeletePostResponse(
            detail=f"Post {post_id} deleted successfully"
        )
