
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, func, delete
from fastapi import HTTPException

from app.models.dataset import Dataset, Item
from app.schemas.datasets import DatasetCreate
from .utils import get_dataset_or_404, check_dataset_name_unique


class DatasetRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def create(self, dataset: DatasetCreate) -> Dataset:
        async with self.session_maker() as session:
            await check_dataset_name_unique(session, dataset.name)
            db_dataset = Dataset(name=dataset.name, description=dataset.description)
            session.add(db_dataset)
            await session.commit()
            await session.refresh(db_dataset)
            return db_dataset

    async def get_all(self) -> list[Dataset]:
        async with self.session_maker() as session:
            stmt = (
                select(Dataset, func.count(Item.id).label("item_count"))
                .outerjoin(Item)
                .group_by(Dataset.id)
            )
            result = await session.execute(stmt)
            datasets = []
            for dataset, item_count in result.all():
                dataset.count = item_count
                datasets.append(dataset)
            return datasets

    async def get_dataset(self, dataset_id: int) -> Dataset:
        async with self.session_maker() as session:
            dataset = await get_dataset_or_404(session, dataset_id)
            stmt = select(func.count(Item.id)).where(Item.dataset_id == dataset_id)
            result = await session.execute(stmt)
            item_count = result.scalar()
            dataset.count = item_count
            return dataset

    async def get_dataset_by_name(self, name: str) -> Dataset | None:
        async with self.session_maker() as session:
            stmt = select(Dataset).where(Dataset.name == name)
            result = await session.execute(stmt)
            dataset = result.scalar_one_or_none()
            if not dataset:
                raise HTTPException(status_code=404, detail="Dataset not found")
            stmt = select(func.count(Item.id)).where(
                Item.dataset_id == dataset.id
                )
            result = await session.execute(stmt)
            item_count = result.scalar()
            dataset.count = item_count
            return dataset

    async def delete_dataset(self, dataset_id: int):
        async with self.session_maker() as session:
            dataset = await get_dataset_or_404(session, dataset_id)
            await session.execute(delete(Item).where(Item.dataset_id == dataset.id))
            await session.delete(dataset)
            await session.commit()