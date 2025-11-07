# region            -----External Imports-----
from datetime import date

from pydantic import BaseModel, ConfigDict
# endregion

class AddressSchema(BaseModel):
    city: str
    street: str
    building_number: str
    zip_code: str


class CreditCardSchema(BaseModel):
    cc_number: str
    cc_type: str
    exp_date: date


class UserResponseSchema(BaseModel):
    id: int
    ext_id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: AddressSchema | None = None
    credit_card: CreditCardSchema | None = None

    model_config = ConfigDict(from_attributes=True)
