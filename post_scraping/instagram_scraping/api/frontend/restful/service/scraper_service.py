# region				-----External Imports-----
import time
# endregion

# region				-----Internal Imports-----
from .auth import LoginHelper
from .browser import BrowserDriver
from .extractor import PostExtractor
from .pages import ProfilePage, PostPage
# endregion


class InstagramScraperService:
    PROFILE_URL_TEMPLATE = "https://www.instagram.com/{username}/"

    def __init__(
            self,
            login_username: str,
            login_password: str
    ):
        self.login_username = login_username
        self.login_password = login_password

    def scrape_posts(
            self,
            target_username: str,
            hashtag: str,
            count: int
    ) -> list:
        driver = BrowserDriver()
        page = driver.start(
            headless=True
        )

        login_helper = LoginHelper(
            page
        )
        login_helper.perform_login(
            "https://www.instagram.com/accounts/login/",
            self.login_username,
            self.login_password
        )

        profile_url = self.PROFILE_URL_TEMPLATE.format(
            username=target_username
        )
        page.goto(
            profile_url
        )
        profile_page = ProfilePage(
            page
        )
        post_links = profile_page.get_post_links(
            count
        )

        posts_data = []
        for link in post_links:
            page.goto(
                link
            )
            post_page = PostPage(
                page
            )
            post_page.wait_for_post()
            time.sleep(
                2
            )
            extractor = PostExtractor(
                page,
                hashtag
            )
            post_data = extractor.extract_post_data()
            posts_data.append(
                post_data.model_dump()
            )

        driver.stop()
        return posts_data
