from datetime import datetime

from pydantic import BaseModel


class WeatherData(BaseModel):
    city: str
    temperature: float
    date: datetime
