from sqlalchemy import and_, select

from app.models import Weather
from app.schemas.weather import WeatherHistoryResponse
from app.services.weather.schemas import WeatherData

from .utils import create_weather_history_response, get_day_datetime_range


class WeatherRepository:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def get_by_date(self, day, config) -> WeatherHistoryResponse:
        async with self.session_maker() as session:
            start_datetime, end_datetime = get_day_datetime_range(day)

            query = (
                select(Weather)
                .where(
                    and_(
                        Weather.city == config.weather.city,
                        Weather.date >= start_datetime,
                        Weather.date <= end_datetime,
                    )
                )
                .order_by(Weather.date)
            )

            result = await session.execute(query)
            weather_records = result.scalars().all()

            return create_weather_history_response(
                weather_records, config.weather.city, day
            )

    async def add_weather(self, weather_data: WeatherData) -> int:
        async with self.session_maker() as session:
            weather_record = Weather(
                city=weather_data.city,
                temperature=weather_data.temperature,
                date=weather_data.date,
            )
            session.add(weather_record)
            await session.commit()
            await session.refresh(weather_record)
            return weather_record.id
