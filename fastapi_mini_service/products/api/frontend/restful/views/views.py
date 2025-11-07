# region				-----External Imports-----
from fastapi import APIRouter
from fastapi_restful.cbv import cbv
import typing
# endregion

# region				-----Internal Imports-----
from .. import schemas
from ..service import ProductService
from ..... import tasks
# endregion

# region			  -----Supporting Variables-----
# endregion


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@cbv(
    router
)
class ProductView:
    product_service: typing.ClassVar[ProductService] = ProductService()

    @router.post(
        "/",
        response_model=schemas.ProductResponseSchema
    )
    async def create_product(
            self,
            product: schemas.ProductCreateSchema
    ):
        new_product = await self.product_service.create_product(
            **product.model_dump()
        )
        return schemas.ProductResponseSchema.from_orm(
            new_product
        )

    @router.get(
        "/",
        response_model=list[schemas.ProductResponseSchema]
    )
    async def get_products(
            self
    ):
        products = await self.product_service.get_products()
        return [schemas.ProductResponseSchema.from_orm(
            p
        ) for p in products]

    @router.get(
        "/{product_id}",
        response_model=schemas.ProductResponseSchema
    )
    async def get_product(
            self,
            product_id: int
    ):
        product = await self.product_service.get_product_by_id(
            product_id
        )
        return schemas.ProductResponseSchema.from_orm(
            product
        )

    @router.put(
        "/{product_id}",
        response_model=schemas.ProductResponseSchema
    )
    async def update_product(
            self,
            product_id: int,
            product: schemas.ProductUpdateSchema
    ):
        updated_product = await self.product_service.update_product(
            product_id,
            **product.model_dump(
                exclude_unset=True
            )
        )
        return schemas.ProductResponseSchema.from_orm(
            updated_product
        )

    @router.delete(
        "/{product_id}",
        response_model=dict
    )
    async def delete_product(
            self,
            product_id: int
    ):
        return await self.product_service.delete_product(
            product_id
        )

    @router.post(
        "/fetch_external/",
        response_model=list[schemas.ProductResponseSchema]
    )
    async def fetch_external_products(
            self,
            payload: schemas.ExternalProductFetchSchema
    ):
        products = await (
            self.product_service.fetch_external_products(
                payload.external_ids
            ))
        return [schemas.ProductResponseSchema.from_orm(
            product
        ) for product in products]

    @router.post(
        "/refresh_all/",
        response_model=dict,
        status_code=202
    )
    async def refresh_all_products(
            self
            ):
        task = tasks.refresh_all_products_task.delay()
        return {
            "detail": "Refreshing all products has started.",
            "task_id": task.id
        }