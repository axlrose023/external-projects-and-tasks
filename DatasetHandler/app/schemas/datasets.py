from typing import Optional
from pydantic import BaseModel, ConfigDict

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None

class DatasetCreate(DatasetBase):
    pass

class DatasetOut(DatasetBase):
    id: int
    count: int = 0

class ItemBase(BaseModel):
    data: dict

class ItemCreate(ItemBase):
    dataset_id: int

class ItemResponse(ItemBase):
    id: int
    dataset_id: int

    model_config = ConfigDict(from_attributes=True)