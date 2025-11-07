from datetime import datetime

import pytest

from app.models import Weather


@pytest.fixture
async def sample_weather_data(test_db):
    async with test_db() as session:
        weather_records = [
            Weather(
                city="TestCity",
                temperature=20.5,
                date=datetime(2024, 1, 15, 10, 0, 0),
                created_at=datetime(2024, 1, 15, 10, 0, 0),
            ),
            Weather(
                city="TestCity",
                temperature=22.0,
                date=datetime(2024, 1, 15, 11, 0, 0),
                created_at=datetime(2024, 1, 15, 11, 0, 0),
            ),
            Weather(
                city="TestCity",
                temperature=18.5,
                date=datetime(2024, 1, 15, 12, 0, 0),
                created_at=datetime(2024, 1, 15, 12, 0, 0),
            ),
        ]

        for record in weather_records:
            session.add(record)

        await session.commit()

        return weather_records
