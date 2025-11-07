import httpx
from typing import Optional

from .settings import Settings
from .services.datasets import DatasetsService
from .exceptions import handle_api_error


class FancyDataClient:
    def __init__(self, api_url: str, api_key: str):
        self.settings = Settings(api_base_url=api_url.rstrip('/'), api_key=api_key)
        self._http_client = httpx.AsyncClient(
            headers={"x-api-key": self.settings.api_key},
            follow_redirects=True
        )
        self.datasets = DatasetsService(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._http_client.aclose()

    async def _post(self, endpoint: str, json: Optional[dict] = None) -> dict:
        full_url = f"{self.settings.api_base_url}{endpoint}"
        resp = await self._http_client.post(full_url, json=json)
        handle_api_error(resp)
        return resp.json()

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict | list:
        full_url = f"{self.settings.api_base_url}{endpoint}"
        resp = await self._http_client.get(full_url, params=params)
        handle_api_error(resp)
        return resp.json()