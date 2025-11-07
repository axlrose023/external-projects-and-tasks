# region            -----External Imports-----
from django.db import transaction
from website.settings.third_party.random_data import settings
# endregion

# region            -----Internal Imports-----
from ...models import Address, User
from ..utils.requester import Requester
# endregion

# region            -----Supporting Variables-----
# endregion
class AddressService:
    def __init__(self, requester: Requester = None):
        self.requester = requester or Requester(settings.request_timeout)
        self.url = settings.address_url

    def fill_missing(self) -> int:
        users = User.objects.filter(address__isnull=True)
        created = 0
        with transaction.atomic():
            for user in users:
                data = self.requester.make_request(self.url)
                Address.objects.create(
                    user=user,
                    city=data["city"],
                    street=data["street_name"],
                    building_number=data["building_number"],
                    zip_code=data["zip_code"]
                )
                created += 1
        return created
    # endregion
