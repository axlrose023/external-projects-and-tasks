from abc import ABC, abstractmethod
from typing import Any

from fastapi import Header, HTTPException

from app.config.config import create_application_config
from app.services.weather.service import WeatherService


class Stub:
    """
    Stub class for FastAPI DI system,
    which allows to use `Depends` without any real dependencies in the code.
    """


class BaseInject(ABC):
    """
    A base abstract class for dependency injection.

    The `BaseInject` class should be inherited by other classes that provide specific implementations of dependency
    injection.
    The inherited classes should implement the `__call__` method with the desired logic for the injection.

    Notes:
    - This class is an abstract base class and should not be instantiated directly.
    - The `__call__` method should be implemented by inheriting classes.
    - The return type of the `__call__` method should be specified in the implementation as specified by the `->
    Any` type hint.
    """

    @abstractmethod
    async def __call__(self) -> Any:
        pass


class InjectStatic(BaseInject):
    """Class for injecting static values into an async function."""

    def __init__(self, target: Any) -> None:
        self.target = target

    async def __call__(self) -> Any:
        return self.target


class InjectContextManager(BaseInject):
    """Class for injecting value from context manager into an async function."""

    def __init__(self, target: Any) -> None:
        self.target = target

    async def __call__(self) -> Any:
        async with self.target() as value:
            yield value


class AppConfigStub(Stub):
    pass


class DatabaseStub(Stub):
    pass


class SessionStub(Stub):
    pass


class DatabaseRepositoryStub(Stub):
    pass


class WeatherTokenStub(Stub):
    pass


class WeatherTokenValidator(BaseInject):
    def __init__(self, config: Any) -> None:
        self.config = config

    async def __call__(self, x_token: str = Header(...)) -> str:
        if x_token != self.config.weather.api_token:
            raise HTTPException(status_code=401, detail={"error": "Invalid token"})
        return x_token


class WeatherServiceStub(Stub):
    pass


def get_weather_service() -> WeatherService:
    config = create_application_config()
    return WeatherService(config.weather)


def get_app_config():
    return create_application_config()
