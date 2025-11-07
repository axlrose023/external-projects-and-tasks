import httpx

from app.config.config import WeatherConfig


class HttpClient:
    def __init__(self, config: WeatherConfig):
        self.timeout = config.timeout

    async def get(self, url: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
