from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config.config import ConfigDTO

@dataclass(frozen=True)
class Database:
    engine: AsyncEngine
    async_session_maker: async_sessionmaker[AsyncSession]

    @classmethod
    def create(
        cls,
        dsn: str,
        pool_size: int = 20,
        max_overflow: int = 20,
        pool_recycle: int = 60,
        pool_timeout: int = 3,
    ) -> "Database":
        engine = create_async_engine(
            dsn,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            pool_timeout=pool_timeout,
        )
        async_session_maker = async_sessionmaker(
            bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
        )
        return cls(engine=engine, async_session_maker=async_session_maker)

def setup_database(config: ConfigDTO):
    return Database.create(
        dsn=config.postgres.dsn,
        pool_size=config.postgres.pool_size,
        max_overflow=config.postgres.pool_max_overflow,
        pool_recycle=config.postgres.pool_recycle,
        pool_timeout=config.postgres.pool_timeout,
    )