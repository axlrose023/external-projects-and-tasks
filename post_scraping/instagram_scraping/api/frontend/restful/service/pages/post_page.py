class PostPage:

    ARTICLE_SELECTOR = "article"

    def __init__(self, page):
        self.page = page

    def wait_for_post(self):
        self.page.wait_for_selector(self.ARTICLE_SELECTOR, timeout=15000)
