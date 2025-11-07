import pytest
from fastapi import FastAPI

from app.api.routes import router
from app.dependencies.database import DatabaseRepositoryStub
from app.dependencies.auth import get_api_key

from app.repository.dataset.dataset_repo import DatasetRepository
from app.repository.dataset_items.items_repo import ItemRepository


@pytest.fixture(scope="function")
def app(session_maker, api_key) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    def _override_db_repo():
        class Repo:
            def __init__(self, sm):
                self.dataset = DatasetRepository(sm)
                self.items = ItemRepository(sm)
        return Repo(session_maker)

    async def _override_get_api_key():
        return api_key

    app.dependency_overrides[DatabaseRepositoryStub] = _override_db_repo
    app.dependency_overrides[get_api_key] = _override_get_api_key
    return app


@pytest.fixture(scope="function")
async def async_client(app):
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
