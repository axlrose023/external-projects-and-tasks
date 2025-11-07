from fastapi import FastAPI

from app.config.config import create_application_config
from app.database.session import setup_database
from app.dependencies.database import DatabaseRepositoryStub
from app.api.routes import router

def create_app() -> FastAPI:
    config = create_application_config()

    database = setup_database(config=config)

    app = FastAPI(title="FancyData API")

    app.include_router(router, prefix="/api")

    app.dependency_overrides[DatabaseRepositoryStub] = (
        lambda: DatabaseRepositoryStub.create(database.async_session_maker)
    )

    app.state.config = config
    app.state.database = database

    return app


app = create_app()
