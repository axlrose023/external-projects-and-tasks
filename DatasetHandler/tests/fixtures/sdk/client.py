import pytest
from fastapi import FastAPI

from app.api.routes import router as api_router

from app.dependencies.database import DatabaseRepositoryStub
from app.dependencies.auth import get_api_key

from app.repository.dataset.dataset_repo import DatasetRepository
from app.repository.dataset_items.items_repo import ItemRepository

from sdk.fancyds.client import FancyDataClient


@pytest.fixture(scope="function")
def sdk_app(session_maker, api_key) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api")

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
async def fancy_client(sdk_app, api_key):

    import httpx
    from httpx import ASGITransport

    client = FancyDataClient(api_url="http://testserver/api", api_key=api_key)

    transport = ASGITransport(app=sdk_app)
    client._http_client = httpx.AsyncClient(
        transport=transport,
        headers={"x-api-key": api_key},
        follow_redirects=True,
    )

    try:
        yield client
    finally:
        await client.close()
