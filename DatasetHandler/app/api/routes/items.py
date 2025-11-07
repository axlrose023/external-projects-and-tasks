from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import get_api_key
from app.dependencies.database import DatabaseRepositoryStub
from app.repository.database.base import DatabaseRepository
from app.schemas import ItemCreate, ItemResponse

router = APIRouter()

@router.post("/", response_model=List[ItemResponse], status_code=status.HTTP_201_CREATED)
async def add_items(
    dataset_id: int,
    items: List[ItemCreate],
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    return await db_repo.items.add_batch(dataset_id, items)

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    dataset_id: int,
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return await db_repo.items.get_paginated(dataset_id, limit, offset)