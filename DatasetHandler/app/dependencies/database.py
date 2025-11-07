
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.repository.database.base import DatabaseRepository

class DatabaseRepositoryStub:
    @classmethod
    def create(cls, session_maker: async_sessionmaker[AsyncSession]):
        return DatabaseRepository.create(session_maker=session_maker)