# region				-----External Imports-----
import typing
import fastapi
from django.core.cache import cache
# endregion

# region				-----Internal Imports-----
from ..... import models
# endregion


class DeletePostService:
    async def delete_post(
            self,
            post_id: int,
            user: typing.Any
    ) -> None:
        post = await models.Post.objects.filter(
            id=post_id,
            user=user
        ).afirst()
        if not post:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        await post.adelete()
        self._invalidate_cache(
            user
        )

    def _invalidate_cache(
            self,
            user: typing.Any
    ) -> None:
        cache_key = f"user_{user.id}_posts"
        cache.delete(
            cache_key
        )
