# region				-----External Imports-----
from playwright.sync_api import sync_playwright
# endregion

# region				-----Internal Imports-----
# endregion

class BrowserDriver:
    def __init__(
            self
    ):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(
            self,
            headless: bool = True
    ):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    def go_to(
            self,
            url: str
    ):
        self.page.goto(
            url
        )

    def wait_for(
            self,
            selector: str,
            timeout: int = 15000
    ):
        self.page.wait_for_selector(
            selector,
            timeout=timeout
        )

    def stop(
            self
    ):
        self.browser.close()
        self.playwright.stop()
