from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    temperature: float
    date: datetime
    created_at: datetime


class WeatherHistoryResponse(BaseModel):
    city: str
    date: str
    temperatures: list[WeatherResponse]
