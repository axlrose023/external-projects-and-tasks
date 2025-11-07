import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.dataset import Dataset

@pytest.fixture(scope="function")
async def engine() -> AsyncEngine:
    eng = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
        echo=False,
        poolclass=StaticPool,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Dataset.metadata.create_all)
    try:
        yield eng
    finally:
        async with eng.begin() as conn:
            await conn.run_sync(Dataset.metadata.drop_all)
        await eng.dispose()

@pytest.fixture(scope="function")
def session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)
