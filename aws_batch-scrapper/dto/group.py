from dataclasses import dataclass


@dataclass
class GroupDTO:
    group_id: str
    last_post_id: str | None

    @property
    def group_link(self) -> str:
        return f"https://www.facebook.com/groups/{self.group_id}?sorting_setting=CHRONOLOGICAL"

    @property
    def last_post_link(self) -> str | None:
        if not self.last_post_id:
            return None
        return f"https://www.facebook.com/groups/{self.group_id}/posts/{self.last_post_id}"
