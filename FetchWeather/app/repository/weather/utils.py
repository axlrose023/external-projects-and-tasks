from datetime import date, datetime

from fastapi import HTTPException

from app.schemas.weather import WeatherHistoryResponse, WeatherResponse


def get_day_datetime_range(day: str) -> tuple[datetime, datetime]:
    if not day or len(day.split("-")) != 3:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid date format. Use Y-m-d format (e.g., 2024-01-15)"
            },
        )

    target_date = date.fromisoformat(day)
    start_datetime = datetime.combine(target_date, datetime.min.time())
    end_datetime = datetime.combine(target_date, datetime.max.time())

    return start_datetime, end_datetime


def create_weather_history_response(
    weather_records, city: str, date: str
) -> WeatherHistoryResponse:
    return WeatherHistoryResponse(
        city=city,
        date=date,
        temperatures=[
            WeatherResponse.model_validate(record) for record in weather_records
        ],
    )
