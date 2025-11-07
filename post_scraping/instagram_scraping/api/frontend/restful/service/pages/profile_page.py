class ProfilePage:

    POST_LINK_SELECTOR = "a[href*='/p/']"

    def __init__(self, page):
        self.page = page

    def get_post_links(self, count: int) -> list:
        self.page.wait_for_selector(self.POST_LINK_SELECTOR, timeout=15000)
        post_links = self.page.eval_on_selector_all(
            self.POST_LINK_SELECTOR,
            "elements => Array.from(new Set(elements.map(el => el.href)))"
        )
        return post_links[:count]
