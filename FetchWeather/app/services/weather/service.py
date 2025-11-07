from datetime import datetime

from app.config.config import WeatherConfig
from app.services.weather.client import HttpClient
from app.services.weather.schemas import WeatherData


class WeatherService:
    def __init__(self, config: WeatherConfig):
        self.config = config
        self.client = HttpClient(config)

    async def get_weather(self, url: str, params: dict) -> WeatherData:
        response = await self.client.get(url, params)
        return self._extract_weather_data(response)

    def _extract_weather_data(self, response: dict) -> WeatherData:
        current = response["current_condition"][0]
        city_name = response["nearest_area"][0]["areaName"][0]["value"]

        date_str = current["localObsDateTime"]
        date = datetime.strptime(date_str, "%Y-%m-%d %I:%M %p")

        return WeatherData(
            city=city_name, temperature=float(current["temp_C"]), date=date
        )
