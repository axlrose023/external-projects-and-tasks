import sys
from pathlib import Path
from typing import Literal

import orjson
import structlog
from pydantic import BaseModel, Field, ValidationError

logger = structlog.get_logger()

DEFAULT_CONFIG_FILENAME = "config.json"
CONFIG_PATH = Path(__file__).parent.parent.parent / DEFAULT_CONFIG_FILENAME

class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field("DEBUG")

class PostgresConfig(BaseModel):
    dsn: str
    pool_size: int = 20
    pool_max_overflow: int = 20
    pool_recycle: int = 60
    pool_timeout: int = 3

class ApiKeyConfig(BaseModel):
    secret_key: str

class ConfigDTO(BaseModel):
    postgres: PostgresConfig
    api_key: ApiKeyConfig
    logging: LoggingConfig = LoggingConfig()

def create_application_config() -> ConfigDTO:
    if not CONFIG_PATH.exists():
        logger.critical("Config file not found.")
        sys.exit(2)
    try:
        config_data = orjson.loads(CONFIG_PATH.read_bytes())
        return ConfigDTO(**config_data)
    except (orjson.JSONDecodeError, ValidationError):
        logger.exception("Config file error.")
        sys.exit(2)