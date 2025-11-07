from __future__ import annotations

from typing import Optional, AsyncIterator

from ..models.dataset import Dataset


class DatasetsService:
    def __init__(self, client: FancyDataClient):
        self.client = client

    async def create(self, name: str, description: Optional[str] = None) -> Dataset:
        payload = {"name": name, "description": description}
        data = await self.client._post(self.client.settings.datasets_create_endpoint, json=payload)
        return Dataset.from_dict(data, self.client)

    async def get(self, identifier: str | int) -> Dataset:
        if isinstance(identifier, int):
            endpoint = self.client.settings.datasets_get_by_id_endpoint.format(id=identifier)
            data = await self.client._get(endpoint)
        else:
            endpoint = self.client.settings.datasets_get_by_name_endpoint.format(name=identifier)
            data = await self.client._get(endpoint)
        return Dataset.from_dict(data, self.client)

    async def __aiter__(self) -> AsyncIterator[Dataset]:
        data = await self.client._get(self.client.settings.datasets_list_endpoint)
        for dataset in data:
            yield Dataset.from_dict(dataset, self.client)

    async def filter(self, name_contains: Optional[str] = None) -> AsyncIterator[Dataset]:
        async for dataset in self:
            if name_contains and name_contains.lower() in dataset.name.lower():
                yield dataset