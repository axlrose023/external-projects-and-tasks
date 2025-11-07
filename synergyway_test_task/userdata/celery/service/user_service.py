# region            -----External Imports-----
from django.db import transaction
from website.settings.third_party.random_data import settings
# endregion

# region            -----Internal Imports-----
from ...models import User
from ..utils.requester import Requester
# endregion

# region            -----Supporting Variables-----
# endregion


class UserService:

    def __init__(self, requester: Requester | None = None) -> None:
        self.requester = requester or Requester(settings.request_timeout)
        self.url = settings.users_url

    def fetch_and_upsert(self) -> int:
        raw_users = self.requester.make_request(self.url)
        created = 0
        with transaction.atomic():
            for data in raw_users:
                _, is_new = User.objects.update_or_create(
                    ext_id=data["id"],
                    defaults={
                        "name": data["name"],
                        "username": data["username"],
                        "email": data["email"],
                        "phone": data.get("phone", ""),
                        "website": data.get("website", "")
                    }
                )
                created += int(is_new)
        return created