from __future__ import annotations

import pandas as pd
from typing import Dict, Any, List, AsyncIterator

from ..models.item import ItemResponse
from ..utils import convert_np_to_lists


class ItemsService:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        if self.dataset.id is None:
            raise ValueError("Dataset must be created first")

    async def add(self, data: Dict[str, Any]):
        await self.add_batch([data])

    async def add_batch(self, data_list: List[Dict[str, Any]]) -> List[ItemResponse]:
        payload = [
            {"dataset_id": self.dataset.id, "data": convert_np_to_lists(d)}
            for d in data_list
        ]
        endpoint = self.dataset.client.settings.items_batch_endpoint.format(dataset_id=self.dataset.id)
        j = await self.dataset.client._post(endpoint, json=payload)
        if isinstance(j, list):
            return [ItemResponse.model_validate(i) for i in j]
        return []

    async def add_from_pandas(self, df: pd.DataFrame):
        data_list = df.to_dict(orient="records")
        await self.add_batch(data_list)

    async def __aiter__(self) -> AsyncIterator[Dict[str, Any]]:
        offset = 0
        limit = 100
        while True:
            batch = await self._fetch_batch(limit, offset)
            if not batch:
                break
            for item in batch:
                yield item["data"]
            offset += limit

    async def iter_batches(self, batch_size: int = 100) -> AsyncIterator[List[Dict[str, Any]]]:
        offset = 0
        while True:
            batch = await self._fetch_batch(batch_size, offset)
            if not batch:
                break
            yield [item["data"] for item in batch]
            offset += batch_size

    async def _fetch_batch(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        endpoint = self.dataset.client.settings.items_endpoint.format(dataset_id=self.dataset.id)
        data = await self.dataset.client._get(
            endpoint,
            params={"limit": limit, "offset": offset}
        )
        return data

    async def filter(self, **kwargs) -> AsyncIterator[Dict[str, Any]]:
        async for item in self:
            match = True
            for key, value in kwargs.items():
                if '__gte' in key:
                    field = key.replace('__gte', '')
                    if item.get(field, 0) < value:
                        match = False
            if match:
                yield item