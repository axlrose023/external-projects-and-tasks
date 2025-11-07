import os
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

LogLevelType: TypeAlias = Literal[
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
]


class LoggingConfig(BaseModel):
    mode: Literal["generic", "json"] = Field("generic", description="Logging mode")
    level: LogLevelType = Field("DEBUG", description="Logging level")


class WebServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    docs: bool = True
    ssl: bool = False


class WeatherConfig(BaseModel):
    city: str = "Kyiv"
    api_url: str = "https://wttr.in"
    timeout: int = 10
    api_token: str = "sk-7f8a9b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"


class PostgresConfigDTO(BaseModel):
    dsn: str = Field(
        default_factory=lambda: f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    pool_size: int = 20
    pool_max_overflow: int = 20
    pool_recycle: int = 60
    pool_timeout: int = 3
    connection_timeout: int = 5
    echo: bool = False


class ConfigDTO(BaseModel):
    web_server: WebServerConfig = WebServerConfig()
    postgres: PostgresConfigDTO = PostgresConfigDTO()
    weather: WeatherConfig = WeatherConfig()
    logging: LoggingConfig = LoggingConfig()


def create_application_config() -> ConfigDTO:
    return ConfigDTO()
