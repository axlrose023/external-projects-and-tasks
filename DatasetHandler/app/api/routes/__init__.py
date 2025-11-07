from fastapi import APIRouter
from .datasets import router as datasets_router
from .items import router as items_router

router = APIRouter()

router.include_router(datasets_router, prefix="/datasets", tags=["dataset"])

router.include_router(items_router, prefix="/datasets/{dataset_id}/items", tags=["items"])
