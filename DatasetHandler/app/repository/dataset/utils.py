from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.dataset import Dataset

async def get_dataset_or_404(session: AsyncSession, dataset_id: int) -> Dataset:
    result = await session.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

async def check_dataset_name_unique(session: AsyncSession, name: str):
    result = await session.execute(select(Dataset).where(Dataset.name == name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Dataset name already exists")