# region            -----External Imports-----
from pydantic_settings import BaseSettings
# endregion

# region            -----Internal Imports-----
# endregion

# region            -----Supporting Variables-----
# endregion


class APISettings(BaseSettings):
    users_url: str = "https://jsonplaceholder.typicode.com/users"
    address_url: str = "https://random-data-api.com/api/address/random_address"
    credit_card_url: str = \
        "https://random-data-api.com/api/business_credit_card/random_card"
    request_timeout: int = 10


settings = APISettings()
