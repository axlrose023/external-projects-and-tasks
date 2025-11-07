from typing import Dict, Any

from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: int
    dataset_id: int
    data: Dict[str, Any]