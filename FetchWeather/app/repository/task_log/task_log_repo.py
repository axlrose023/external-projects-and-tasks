from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.schemas.enums import TaskStatus


class TaskLogRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def log_success(self, weather_id: int) -> None:
        from app.models import TaskLog

        async with self.session_maker() as session:
            task_log = TaskLog(
                weather_id=weather_id,
                status=TaskStatus.SUCCESS,
                details=None,
            )
            session.add(task_log)
            await session.commit()

    async def log_failure(self, weather_id: int | None, details: str) -> None:
        from app.models import TaskLog

        async with self.session_maker() as session:
            task_log = TaskLog(
                weather_id=weather_id,
                status=TaskStatus.FAILURE,
                details=details,
            )
            session.add(task_log)
            await session.commit()
