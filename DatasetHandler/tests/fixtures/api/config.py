import pytest
from app.config import create_application_config

@pytest.fixture(scope="session")
def app_config():
    return create_application_config()

@pytest.fixture(scope="session")
def api_key(app_config) -> str:
    return app_config.api_key.secret_key

@pytest.fixture
def auth_headers(api_key):
    return {"X-API-Key": api_key}

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"