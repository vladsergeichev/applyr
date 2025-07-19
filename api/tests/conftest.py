from collections.abc import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from faker import Faker
from fastapi import FastAPI

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import create_test_apply_data, create_test_user_data
from tests.factories.base_factories import ApplyFactory, UserFactory


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Бэкенд для асинхронных тестов"""
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    """Фикстура для event loop с session scope"""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def lifespanned_app(event_loop) -> AsyncIterator[FastAPI]:
    """Фикстура для управления жизненным циклом FastAPI приложения"""
    from main import app

    async with LifespanManager(app):
        yield app


@pytest.fixture(scope="session")
def faker() -> Faker:
    """Фикстура для генерации тестовых данных"""
    return Faker(locale=["ru_RU", "en_US"])


@pytest.fixture(scope="session")
async def async_client(lifespanned_app: FastAPI) -> AsyncTestAPIClient:
    """Фикстура для асинхронного API клиента"""
    return AsyncTestAPIClient.build_app_client(app=lifespanned_app)


@pytest.fixture
def user_factory(faker: Faker) -> UserFactory:
    """Фикстура для фабрики пользователей"""
    return UserFactory()


@pytest.fixture
def apply_factory(faker: Faker) -> ApplyFactory:
    """Фикстура для фабрики откликов"""
    return ApplyFactory()


@pytest.fixture
def test_user_data(user_factory: UserFactory) -> dict:
    """Фикстура для тестовых данных пользователя"""
    return user_factory.build_user_data()


@pytest.fixture
def test_user_data_with_faker(faker: Faker) -> dict:
    """Фикстура для тестовых данных пользователя с использованием Faker"""
    return create_test_user_data(faker)


@pytest.fixture
async def test_user_with_token(async_client: AsyncTestAPIClient) -> tuple[dict, str]:
    """Фикстура для создания тестового пользователя с токеном"""
    return await async_client.create_test_user()


@pytest.fixture
def test_apply_data(apply_factory: ApplyFactory) -> dict:
    """Фикстура для тестовых данных отклика"""
    return apply_factory.build_apply_data()


@pytest.fixture
def test_apply_data_with_faker(faker: Faker) -> dict:
    """Фикстура для тестовых данных отклика с использованием Faker"""
    return create_test_apply_data(faker)


@pytest.fixture
def test_vacancy_data(apply_factory: ApplyFactory) -> dict:
    """Фикстура для тестовых данных вакансии"""
    return apply_factory.build_vacancy_data()


@pytest.fixture
def authorized_client(
    async_client: AsyncTestAPIClient, test_user_with_token: tuple[dict, str]
) -> AsyncTestAPIClient:
    """Фикстура для авторизованного клиента"""
    user_data, access_token = test_user_with_token
    return AsyncTestAPIClient.build_authorized_app_client(
        app=async_client._transport.app,  # type: ignore
        access_token=access_token,
    )
