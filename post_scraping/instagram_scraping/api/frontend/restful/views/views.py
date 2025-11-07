# region				-----External Imports-----
import asyncio
import fastapi
from fastapi_utils.cbv import cbv
from instagram_scraping.tasks import scrape_instagram
# endregion

# region				-----Internal Imports-----
from .. import schemas
# endregion


# region			  -----Supporting Variables-----
router = fastapi.APIRouter(
    prefix="/instagram",
    tags=["Instagram"]
)
# endregion

# region			  -----Views-----
@cbv(
    router
)
class InstagramScraperView:
    @router.post(
        path="/scrape",
        status_code=fastapi.status.HTTP_200_OK,
        response_model=schemas.ScrapedPostsResponseSchema
    )
    async def start_and_wait_scrape(
            self,
            payload: schemas.ScrapeRequestSchema
    ):
        task = scrape_instagram.delay(
            payload.login_username,
            payload.login_password,
            payload.target_username,
            payload.hashtag,
            payload.count
        )
        result = await asyncio.to_thread(
            task.get,
            timeout=300
        )
        return schemas.ScrapedPostsResponseSchema(
            posts=result
        )
# endregion