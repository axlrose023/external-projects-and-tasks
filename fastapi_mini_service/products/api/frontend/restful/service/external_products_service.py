# region				-----External Imports-----
import asyncio
from typing import List
from django.db import IntegrityError
# endregion

# region				-----Internal Imports-----
from .. import schemas
from .api_client import ExternalProductAPIClient
from .product_repository import ProductRepository
# endregion

# region			  -----Supporting Variables-----
# endregion

class ExternalProductService:
    def __init__(
            self
    ):
        self.repository = ProductRepository()

    async def fetch_products(
            self,
            external_ids: List[int]
    ) -> List[dict]:
        async with ExternalProductAPIClient() as client:
            tasks = [client.fetch_product(
                external_id
            ) for external_id in external_ids]
            responses = await asyncio.gather(
                *tasks,
                return_exceptions=True
            )
            return responses

    def validate_products(
            self,
            responses: List[dict]
    ) -> List[schemas.ExternalProductSchema]:
        return schemas.ExternalProductSchema.parse_many(
            responses
        )

    async def store_products(
            self,
            validated_products: List[schemas.ExternalProductSchema]
    ) -> List:
        results = []

        for product in validated_products:
            data = product.model_dump()
            try:
                result = await self.repository.create(
                    data
                )
            except IntegrityError:
                result = await self.repository.update_by_external_id(
                    external_id=data["external_id"],
                    data=data
                )
            results.append(
                result
            )

        return results

    async def fetch_and_update_external_products(
            self,
            external_ids: List[int]
    ) -> List:
        responses = await self.fetch_products(
            external_ids
        )
        validated_products = self.validate_products(
            responses
        )
        return await self.store_products(
            validated_products
        )

    async def get_all_external_ids(
            self
    ) -> List[int]:
        products = await self.repository.get_all_with_external_id()
        return [product.external_id for product in products]

    async def update_existing_products(
            self,
            validated_products: List[schemas.ExternalProductSchema]
    ) -> List:
        update_tasks = [
            self.repository.update_by_external_id(
                data=product.model_dump(),
                external_id=product.external_id
            )
            for product in validated_products
        ]
        return await asyncio.gather(
            *update_tasks
        )

    async def get_and_update_all_external_products(
            self
    ) -> List:

        external_ids = await self.get_all_external_ids()

        if not external_ids:
            return []

        responses = await self.fetch_products(
            external_ids
        )
        validated_products = self.validate_products(
            responses
        )

        await self.update_existing_products(
            validated_products
        )
