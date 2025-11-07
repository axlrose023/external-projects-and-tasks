from typing import Annotated, List
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_api_key
from app.dependencies.database import DatabaseRepositoryStub
from app.repository.database.base import DatabaseRepository
from app.schemas import DatasetCreate, DatasetOut

router = APIRouter()

@router.post("/", response_model=DatasetOut, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    dataset: DatasetCreate,
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    return await db_repo.dataset.create(dataset)

@router.get("/", response_model=List[DatasetOut])
async def list_datasets(
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    return await db_repo.dataset.get_all()

@router.get("/{dataset_id}", response_model=DatasetOut)
async def get_dataset(
    dataset_id: int,
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    return await db_repo.dataset.get_dataset(dataset_id)

@router.get("/name/{name}", response_model=DatasetOut)
async def get_dataset_by_name(
    name: str,
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    return await db_repo.dataset.get_dataset_by_name(name)


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: int,
    db_repo: Annotated[DatabaseRepository, Depends(DatabaseRepositoryStub)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    await db_repo.dataset.delete_dataset(dataset_id)