# region				-----External Imports-----
import pydantic
import typing
import decimal
from datetime import datetime
# endregion

# region				-----Internal Imports-----
# endregion

# region			  -----Supporting Variables-----
# endregion

class ProductCreateSchema(
    pydantic.BaseModel
):
    name: str
    price: decimal.Decimal
    description: typing.Optional[str] = None
    external_id: typing.Optional[int] = None

    @pydantic.field_validator(
        "price"
    )
    def price_must_be_positive(
            cls,
            value
    ):
        if value <= 0:
            raise ValueError(
                "Price must be greater than 0"
            )
        return value

    @pydantic.field_validator(
        "external_id",
        mode="before"
    )
    def validate_external_id(
            cls,
            value
    ):
        if value == 0:
            return None
        return value


class ProductUpdateSchema(
    pydantic.BaseModel
):
    name: typing.Optional[str] = None
    price: typing.Optional[decimal.Decimal] = None
    description: typing.Optional[str] = None
    external_id: typing.Optional[int] = None

    @pydantic.field_validator(
        "price"
    )
    def price_must_be_positive(
            cls,
            value
    ):
        if value is not None and value <= 0:
            raise ValueError(
                "Price must be greater than 0"
            )
        return value

    @pydantic.field_validator(
        "external_id",
        mode="before"
    )
    def validate_external_id(
            cls,
            value
    ):
        if value == 0:
            return None
        return value


class ProductResponseSchema(
    pydantic.BaseModel
):
    id: int
    name: str
    price: decimal.Decimal
    description: typing.Optional[str]
    external_id: typing.Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExternalProductSchema(
    ProductCreateSchema
):
    name: str = pydantic.Field(
        ...,
        alias="title"
    )
    external_id: typing.Optional[int] = pydantic.Field(
        None,
        alias="id"
    )

    class Config:
        populate_by_name = True
        extra = "ignore"

    @classmethod
    def parse_many(
            cls,
            responses: list[dict]
    ) -> list["ExternalProductSchema"]:
        products = []
        for response in responses:
            if not isinstance(
                    response,
                    dict
                    ):
                continue
            product = cls.parse_obj(
                response
            )
            products.append(
                product
            )
        return products


class ExternalProductFetchSchema(
    pydantic.BaseModel
):
    external_ids: typing.Optional[typing.List[int]]

    @pydantic.field_validator(
        "external_ids",
        mode="before"
    )
    def validate_external_ids(
            cls,
            value
    ):
        if not value or value == [0]:
            raise ValueError(
                "external_ids must contain at least one valid id (non-zero)"
            )
        return value
