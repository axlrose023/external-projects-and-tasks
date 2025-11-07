from sqlalchemy.ext.asyncio import async_sessionmaker

from app.repository.task_log.task_log_repo import TaskLogRepository
from app.repository.weather.weather_repo import WeatherRepository


class DatabaseRepository:
    def __init__(
        self,
        weather: WeatherRepository,
        task_log: TaskLogRepository,
    ) -> None:
        self.weather = weather
        self.task_log = task_log

    @classmethod
    def create(
        cls, session_maker: async_sessionmaker | None = None
    ) -> "DatabaseRepository":
        if session_maker:
            return cls(
                weather=WeatherRepository(session_maker=session_maker),
                task_log=TaskLogRepository(session_maker=session_maker),
            )
        return None
