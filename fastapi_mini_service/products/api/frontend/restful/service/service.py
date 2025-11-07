# region				-----External Imports-----
import asyncio
from utils.exceptions import DetailedHTTPException
# endregion

# region				-----Internal Imports-----
from .product_repository import ProductRepository
from .external_products_service import ExternalProductService
# endregion

# region			  -----Supporting Variables-----
# endregion

class ProductService:
    def __init__(
            self
    ):
        self.repository = ProductRepository()
        self.external_product_service = ExternalProductService()

    async def create_product(
            self,
            **data
    ):
        return await self.repository.create(
            data
        )

    async def get_products(
            self
    ):
        return await self.repository.get_all()

    async def get_product_by_id(
            self,
            product_id: int
    ):
        product = await self.repository.get_by_id(
            product_id
        )
        if not product:
            raise DetailedHTTPException(
                status_code=404,
                error_code="PRODUCT_NOT_FOUND",
                detail="Product not found",
                payload={
                    "product_id": product_id
                }
            )
        return product

    async def update_product(
            self,
            product_id: int,
            **data
    ):
        updated_product = await self.repository.update(
            product_id,
            data
        )
        if not updated_product:
            raise DetailedHTTPException(
                status_code=404,
                error_code="PRODUCT_NOT_FOUND",
                detail="Product not found",
                payload={
                    "product_id": product_id
                }
            )
        return updated_product

    async def delete_product(
            self,
            product_id: int
    ):
        success = await self.repository.delete(
            product_id
        )
        if not success:
            raise DetailedHTTPException(
                status_code=404,
                error_code="PRODUCT_NOT_FOUND",
                detail="Product not found",
                payload={
                    "product_id": product_id
                }
            )
        return {
            "detail": f"Product {product_id} deleted successfully"
        }

    async def fetch_external_products(
            self,
            external_ids: list[int]
    ):
        return await (
            self.external_product_service.fetch_and_update_external_products(
                external_ids
            ))

    async def update_all_external_products(
            self
    ):
        return await (
            self.external_product_service
            .get_and_update_all_external_products())
