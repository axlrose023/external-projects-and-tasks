from app.dependencies.stub import get_app_config
from app.repository.database.base import DatabaseRepository
from app.services.weather.service import WeatherService


async def fetch_weather(
    weather_service: WeatherService,
    database_repo: DatabaseRepository,
    config=get_app_config(),
):
    url = f"{config.weather.api_url}/{config.weather.city}"
    params = {"format": "j1", "lang": "ru"}

    weather_data = await weather_service.get_weather(url, params)

    weather_id = await database_repo.weather.add_weather(weather_data)
    return weather_id
