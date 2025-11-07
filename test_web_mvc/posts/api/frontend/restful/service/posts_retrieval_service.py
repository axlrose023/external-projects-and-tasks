# region				-----External Imports-----
import typing
from django.core.cache import cache
# endregion

# region				-----Internal Imports-----
from .. import schemas
from ..... import models
# endregion

class GetPostService:
    _CACHE_TIMEOUT = 300

    async def get_posts(
            self,
            user: typing.Any
    ) -> list:
        cache_key = self._get_cache_key(
            user
        )
        posts = self._get_cached_posts(
            cache_key
        )
        if posts is not None:
            return posts

        posts = await self._fetch_posts_from_db(
            user
        )
        posts = [schemas.PostSchema.model_validate(
            post
        ) for post in posts]
        self._cache_posts(
            cache_key,
            posts
        )
        return posts

    def _get_cache_key(
            self,
            user: typing.Any
    ) -> str:
        return f"user_{user.id}_posts"

    def _get_cached_posts(
            self,
            cache_key: str
    ) -> typing.Optional[list]:
        return cache.get(
            cache_key
        )

    async def _fetch_posts_from_db(
            self,
            user: typing.Any
    ) -> list:
        posts_qs = models.Post.objects.filter(
            user=user
        )
        posts = [post async for post in posts_qs.all()]
        return posts

    def _cache_posts(
            self,
            cache_key: str,
            posts: list
    ) -> None:
        cache.set(
            cache_key,
            posts,
            timeout=self._CACHE_TIMEOUT
        )
