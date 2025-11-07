import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(test_db, test_config):
    app = create_app(application_config=test_config)

    from app.dependencies.stub import DatabaseRepositoryStub, InjectStatic
    from app.repository.database.base import DatabaseRepository

    database_repository = DatabaseRepository.create(session_maker=test_db)
    app.dependency_overrides[DatabaseRepositoryStub] = InjectStatic(database_repository)

    return TestClient(app)
