import pytest

from app.config.config import ConfigDTO, WeatherConfig


@pytest.fixture
def test_config():
    return ConfigDTO(
        weather=WeatherConfig(
            api_token="test-token-32-characters-long-here", city="TestCity"
        )
    )
