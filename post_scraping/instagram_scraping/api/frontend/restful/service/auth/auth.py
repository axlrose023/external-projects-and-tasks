# region				-----External Imports-----
import time
from playwright.sync_api import Page


# endregion

# region				-----Internal Imports-----
# endregion

class LoginHelper:
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    NOT_NOW_BUTTON = "button:has-text('Not Now')"

    def __init__(
            self,
            page: Page
    ):
        self.page = page

    def perform_login(
            self,
            login_url: str,
            username: str,
            password: str
    ):
        self.page.goto(
            login_url
        )
        self.wait_for(
            self.USERNAME_INPUT,
            timeout=10000
        )
        self.page.fill(
            self.USERNAME_INPUT,
            username
        )
        self.page.fill(
            self.PASSWORD_INPUT,
            password
        )
        with self.page.expect_navigation(
                timeout=15000
        ):
            self.page.click(
                self.SUBMIT_BUTTON
            )
        time.sleep(
            5
        )
        try:
            not_now = self.page.query_selector(
                self.NOT_NOW_BUTTON
            )
            if not_now:
                not_now.click()
                time.sleep(
                    2
                )
        except Exception:
            pass

    def wait_for(
            self,
            selector: str,
            timeout: int = 15000
    ):
        self.page.wait_for_selector(
            selector,
            timeout=timeout
        )
