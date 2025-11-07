# region				-----External Imports-----
# endregion

# region				-----Internal Imports-----
from .....models import Product
# endregion

# region			  -----Supporting Variables-----
# endregion

class ProductRepository:
    async def create(
            self,
            data: dict
    ):
        return await Product.objects.acreate(
            **data
        )

    async def get_all(
            self
    ):
        return [product async for product in Product.objects.all()]

    async def get_by_id(
            self,
            product_id: int
    ):
        try:
            return await Product.objects.aget(
                id=product_id
            )
        except Product.DoesNotExist:
            return None

    async def update(
            self,
            product_id: int,
            data: dict
    ):
        product = await self.get_by_id(
            product_id
        )
        if product:
            for key, value in data.items():
                setattr(
                    product,
                    key,
                    value
                )
            await product.asave()
            return product
        return None

    async def delete(
            self,
            product_id: int
    ):
        product = await self.get_by_id(
            product_id
        )
        if product:
            await product.adelete()
            return True
        return False

    async def get_all_with_external_id(
            self
    ):
        return [product async for product in Product.objects.filter(
            external_id__isnull=False
        )]

    async def get_by_external_id(
            self,
            external_id: int
            ):
        try:
            return await Product.objects.aget(
                external_id=external_id
                )
        except Product.DoesNotExist:
            return None

    async def update_by_external_id(
            self,
            external_id: int,
            data: dict
            ):
        product = await self.get_by_external_id(
            external_id
            )
        if product:
            data.pop("external_id",None)
            for key, value in data.items():
                setattr(
                    product,
                    key,
                    value
                    )
            await product.asave()
            return product
        return None
