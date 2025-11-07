from fastapi import APIRouter, Depends

from app.dependencies.stub import (
    AppConfigStub,
    DatabaseRepositoryStub,
    WeatherTokenStub,
)
from app.repository.database.base import DatabaseRepository
from app.schemas.weather import WeatherHistoryResponse

weather_router = APIRouter(prefix="", tags=["Weather"])


@weather_router.get("/weather", response_model=WeatherHistoryResponse)
async def get_weather_history(
    day: str,
    db_repo: DatabaseRepository = Depends(DatabaseRepositoryStub),
    token: str = Depends(WeatherTokenStub),
    config=Depends(AppConfigStub),
):
    return await db_repo.weather.get_by_date(day, config)
