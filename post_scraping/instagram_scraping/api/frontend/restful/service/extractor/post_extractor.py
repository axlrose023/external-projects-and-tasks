# region				-----External Imports-----
from bs4 import BeautifulSoup
import re
# endregion

# region				-----Internal Imports-----
from ...schemas import PostSchema
# endregion

class PostElementFinder:

    DESCRIPTION_SELECTOR = "h1._ap3a._aaco._aacu._aacx._aad7._aade"
    LIKE_SELECTOR = (
        "span.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2."
        "x1i0vuye.xvs91rp.x1s688f.x5n08af.x10wh9bi.x1wdrske.x8viiok."
        "x18hxmgj span"
    )
    COMMENT_SELECTOR = "ul._a9ym li._a9zj"

    def __init__(
            self,
            page
    ):
        self.page = page

    def get_description_html(
            self
    ) -> str:
        elem = self.page.query_selector(
            self.DESCRIPTION_SELECTOR
        )
        return elem.inner_html() if elem else ""

    def get_likes_text(
            self
    ) -> str:
        elem = self.page.query_selector(
            self.LIKE_SELECTOR
        )
        return elem.inner_text() if elem else ""

    def get_comment_elements(
            self
    ):
        return self.page.query_selector_all(
            self.COMMENT_SELECTOR
        )


class PostExtractor:

    def __init__(
            self,
            page,
            hashtag: str
    ):
        self.page = page
        self.hashtag = hashtag
        self.finder = PostElementFinder(
            page
        )

    def extract_post_data(
            self
    ) -> PostSchema:
        description_text, hashtag_count = self._extract_description()
        likes = self._extract_likes()
        comments = self._extract_comments()
        hashtag_present = self.hashtag.lower() in description_text.lower()
        return PostSchema(
            description=description_text,
            likes=likes,
            comments=comments,
            hashtag_present=hashtag_present,
            hashtag_count=hashtag_count
        )

    def _extract_description(
            self
    ) -> (str, int):
        html = self.finder.get_description_html()
        description_text = ""
        hashtag_count = 0
        if html:
            html = re.sub(
                r"<br\s*/?>",
                "\n",
                html
            )
            soup = BeautifulSoup(
                html,
                "html.parser"
            )
            description_text = soup.get_text(
                separator="\n"
            ).strip()
            hashtag_links = soup.find_all(
                "a",
                href=lambda
                    x: x and "/explore/tags/" in x
            )
            hashtag_count = len(
                hashtag_links
            )
        return description_text, hashtag_count

    def _extract_likes(
            self
    ) -> int:
        text = self.finder.get_likes_text()
        likes = 0
        if text:
            likes_numbers = re.findall(
                r'\d+',
                text.replace(
                    "\xa0",
                    ""
                )
            )
            if likes_numbers:
                likes = int(
                    "".join(
                        likes_numbers
                    )
                )
        return likes

    def _extract_comments(
            self
    ) -> int:
        elements = self.finder.get_comment_elements()
        return len(
            elements
        ) if elements else 0
