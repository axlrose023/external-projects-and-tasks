# region            -----External Imports-----
# endregion
from typing import List

from django.db.models import QuerySet

# region            -----Internal Imports-----
from .....models import User
# endregion

# region            -----Supporting Variables-----
# endregion

class UserQueryService:
    async def fetch_all(self) -> List[User]:
        queryset: QuerySet = User.objects.select_related(
            "address", "credit_card"
            ).all()
        return [user async for user in queryset]