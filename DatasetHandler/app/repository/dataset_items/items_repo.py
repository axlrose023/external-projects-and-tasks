from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select

from app.models.dataset import Item
from app.repository.dataset.utils import get_dataset_or_404
from app.schemas import ItemCreate

class ItemRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add_batch(self, dataset_id: int, items: list[ItemCreate]) -> list[Item]:
        async with self.session_maker() as session:
            await get_dataset_or_404(session, dataset_id)
            db_items = [Item(dataset_id=dataset_id, data=item.data) for item in items]
            session.add_all(db_items)
            await session.commit()
            for db_item in db_items:
                await session.refresh(db_item)
            return db_items

    async def get_paginated(self, dataset_id: int, limit: int, offset: int) -> list[Item]:
        async with self.session_maker() as session:
            await get_dataset_or_404(session, dataset_id)
            stmt = select(Item).where(Item.dataset_id == dataset_id).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()