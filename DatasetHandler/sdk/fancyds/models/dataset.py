from __future__ import annotations

from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from ..exceptions import FancyDataError


@dataclass
class Dataset:
    client: FancyDataClient
    name: str
    description: Optional[str] = None
    id: Optional[int] = None
    count: int = 0
    items: "ItemsService" = field(init=False)

    def __post_init__(self):
        from ..services.items import ItemsService
        self.items = ItemsService(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: FancyDataClient) -> "Dataset":
        return cls(
            client=client,
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            count=data.get("count", 0)
        )

    async def create(self):
        if self.id is not None:
            raise FancyDataError("Dataset already created")
        dataset = await self.client.datasets.create(self.name, self.description)
        self.id = dataset.id
        self.count = dataset.count