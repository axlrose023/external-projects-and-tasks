# region				-----External Imports-----
from celery import shared_task
from concurrent.futures import ThreadPoolExecutor
# endregion

# region				-----Internal Imports-----
from ..api.frontend.restful.service import InstagramScraperService
# endregion

# region			  -----Supporting Variables-----
# endregion


@shared_task(
    queue="scrap",
    name="scrape_instagram"
)
def scrape_instagram(
        login_username,
        login_password,
        target_username,
        hashtag,
        count
):
    def run_scraping():
        scraper = InstagramScraperService(
            login_username,
            login_password
        )
        posts = scraper.scrape_posts(
            target_username,
            hashtag,
            count
        )
        return posts

    with ThreadPoolExecutor(
            max_workers=1
    ) as executor:
        future = executor.submit(
            run_scraping
        )
        posts = future.result()
    return posts
