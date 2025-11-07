# region            -----External Imports-----
from django.db import transaction
from website.settings.third_party.random_data import settings
# endregion

# region            -----Internal Imports-----
from ...models import CreditCard, User
from ..utils.requester import Requester
# endregion

# region            -----Supporting Variables-----
# endregion


class CreditCardService:

    def __init__(self, requester: Requester | None = None) -> None:
        self.requester = requester or Requester(settings.request_timeout)
        self.url = settings.credit_card_url

    def fill_missing(self) -> int:
        users = User.objects.filter(credit_card__isnull=True)
        created = 0
        with transaction.atomic():
            for user in users:
                data = self.requester.make_request(self.url)
                CreditCard.objects.create(
                    user=user,
                    cc_number=data["credit_card_number"],
                    cc_type=data["credit_card_type"],
                    exp_date=data["credit_card_expiry_date"]
                )
                created += 1
        return created
    # endregion
