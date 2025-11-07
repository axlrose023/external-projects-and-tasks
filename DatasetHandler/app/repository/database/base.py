from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.repository.dataset.dataset_repo import DatasetRepository
from app.repository.dataset_items.items_repo import ItemRepository


class DatabaseRepository:
    def __init__(
        self,
        dataset: DatasetRepository,
        items: ItemRepository,
    ) -> None:
        self.dataset = dataset
        self.items = items

    @classmethod
    def create(cls, session_maker: async_sessionmaker[AsyncSession]) -> "DatabaseRepository":
        return cls(
            dataset=DatasetRepository(session_maker=session_maker),
            items=ItemRepository(session_maker=session_maker),
        )