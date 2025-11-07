from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from . import SUMMARY
from .api.routes.weather import weather_router
from .config.config import ConfigDTO, create_application_config
from .database.session import setup_database
from .dependencies.stub import (
    AppConfigStub,
    DatabaseRepositoryStub,
    DatabaseStub,
    InjectContextManager,
    InjectStatic,
    SessionStub,
    WeatherTokenStub,
    WeatherTokenValidator,
)
from .repository.database.base import DatabaseRepository
from .services.logging.logging_config import setup_structlog
from .services.weather.task import fetch_weather

logger = structlog.get_logger()


def create_app(
    configure_logging: bool = True,
    application_config: ConfigDTO | None = None,
) -> FastAPI:
    if not application_config:
        application_config = create_application_config()

    if configure_logging:
        setup_structlog(
            mode=application_config.logging.mode,
            level=application_config.logging.level,
        )

    database = setup_database(config=application_config)
    database_repository = DatabaseRepository.create(
        session_maker=database.async_session_maker
    )

    def setup_weather_scheduler():
        from apscheduler.schedulers.asyncio import AsyncIOScheduler

        from app.dependencies.stub import get_weather_service
        from app.services.weather.utils import setup_task_listeners

        weather_service = get_weather_service()

        async def scheduled_task():
            await fetch_weather(weather_service, database_repository)

        scheduler = AsyncIOScheduler()
        scheduler.add_job(scheduled_task, "interval", hours=1, id="weather_fetch")
        setup_task_listeners(scheduler, database_repository)

        return scheduler

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        scheduler = setup_weather_scheduler()
        scheduler.start()
        try:
            yield
        finally:
            scheduler.shutdown()

    application = FastAPI(
        title="Weather API",
        version="1.0.0",
        summary=SUMMARY,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ],
    )

    # Setup dependency injection
    application.dependency_overrides[AppConfigStub] = InjectStatic(application_config)
    application.dependency_overrides[SessionStub] = InjectContextManager(
        database.async_session_maker
    )
    application.dependency_overrides[DatabaseStub] = InjectStatic(database)
    application.dependency_overrides[DatabaseRepositoryStub] = InjectStatic(
        database_repository
    )
    application.dependency_overrides[WeatherTokenStub] = WeatherTokenValidator(
        application_config
    )

    # Include routers
    application.include_router(weather_router)

    # Setup Prometheus metrics
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        application
    ).expose(application, endpoint="/metrics")

    return application


app = create_app()
