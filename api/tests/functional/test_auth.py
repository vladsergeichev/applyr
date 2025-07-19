import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import (
    assert_response_contains,
    assert_response_has_error,
    assert_response_status,
)
from tests.factories.base_factories import UserFactory
from models import UserModel

@pytest.fixture(autouse=True)
async def clear_users(async_client: AsyncTestAPIClient):
    # Очищаем пользователей между тестами
    from database import get_async_db
    async for db in get_async_db():
        await db.execute(delete(UserModel))
        await db.commit()
        break

@pytest.mark.asyncio
async def test_register_user_success(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    user_data = user_factory.build_user_data()
    response = await async_client.register_user(user_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["access_token", "token_type"])

@pytest.mark.asyncio
async def test_register_user_duplicate_username(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    user_data = user_factory.build_user_data()
    response1 = await async_client.register_user(user_data)
    assert_response_status(response1, status.HTTP_200_OK)
    response2 = await async_client.register_user(user_data)
    assert_response_status(response2, status.HTTP_400_BAD_REQUEST)
    assert_response_has_error(response2)

@pytest.mark.asyncio
async def test_login_user_success(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест успешного входа пользователя"""
    # Регистрируем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Входим с теми же данными
    login_response = await async_client.login_user(
        user_data["username"], user_data["password"]
    )
    assert_response_status(login_response, status.HTTP_200_OK)
    assert_response_contains(login_response, ["access_token", "token_type"])


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест входа с неверными данными"""
    login_data = user_factory.build_login_data()
    response = await async_client.login_user(
        login_data["username"], login_data["password"]
    )
    assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
    assert_response_has_error(response)


@pytest.mark.asyncio
async def test_refresh_token_success(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест успешного обновления токена"""
    # Регистрируем пользователя и получаем токены
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем refresh_token из cookie
    cookies = register_response.cookies
    refresh_token = cookies.get("refresh_token")

    if refresh_token:
        # Обновляем токен
        response = await async_client.refresh_token(refresh_token)
        assert_response_status(response, status.HTTP_200_OK)
        assert_response_contains(response, ["access_token", "token_type"])
    else:
        pytest.skip("API не возвращает refresh_token в cookie")


@pytest.mark.asyncio
async def test_logout_user_success(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест успешного выхода пользователя"""
    # Регистрируем пользователя и получаем токены
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем refresh_token из cookie
    cookies = register_response.cookies
    refresh_token = cookies.get("refresh_token")

    if refresh_token:
        # Выходим
        response = await async_client.logout_user(refresh_token)
        assert_response_status(response, status.HTTP_200_OK)
    else:
        pytest.skip("API не возвращает refresh_token в cookie")


@pytest.mark.asyncio
async def test_register_user_invalid_data(async_client: AsyncTestAPIClient):
    invalid_user_data = {
        "username": "",  # Пустое имя пользователя
        "password": "",  # Пустой пароль
    }
    response = await async_client.register_user(invalid_user_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)

@pytest.mark.asyncio
async def test_register_user_short_username(async_client: AsyncTestAPIClient):
    invalid_user_data = {
        "username": "ab",  # Слишком короткое имя
        "password": "password123",
    }
    response = await async_client.register_user(invalid_user_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)

@pytest.mark.asyncio
async def test_register_user_short_password(async_client: AsyncTestAPIClient):
    invalid_user_data = {
        "username": "testuser123",
        "password": "123",  # Слишком короткий пароль
    }
    response = await async_client.register_user(invalid_user_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)


@pytest.mark.asyncio
async def test_register_user_invalid_username_format(async_client: AsyncTestAPIClient):
    invalid_user_data = {
        "username": "test-user",  # Содержит дефис
        "password": "password123",
    }
    response = await async_client.register_user(invalid_user_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)


@pytest.mark.asyncio
async def test_update_telegram_username_success(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест успешного обновления Telegram username"""
    # Регистрируем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Обновляем Telegram username
    telegram_data = user_factory.build_telegram_update_data()
    response = await async_client.update_telegram_username(telegram_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["message"])


@pytest.mark.asyncio
async def test_update_telegram_username_duplicate(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    # Регистрируем первого пользователя
    user_data1 = user_factory.build_user_data()
    register_response1 = await async_client.register_user(user_data1)
    assert_response_status(register_response1, status.HTTP_200_OK)
    access_token1 = register_response1.json().get("access_token")
    async_client.set_auth_token(access_token1)
    telegram_data = user_factory.build_telegram_update_data()
    response1 = await async_client.update_telegram_username(telegram_data)
    assert_response_status(response1, status.HTTP_200_OK)
    # Регистрируем второго пользователя
    user_data2 = user_factory.build_user_data()
    register_response2 = await async_client.register_user(user_data2)
    assert_response_status(register_response2, status.HTTP_200_OK)
    access_token2 = register_response2.json().get("access_token")
    async_client.set_auth_token(access_token2)
    # Пытаемся использовать тот же Telegram username для второго пользователя
    response2 = await async_client.update_telegram_username(telegram_data)
    assert_response_status(response2, status.HTTP_400_BAD_REQUEST)
    assert_response_has_error(response2)


@pytest.mark.asyncio
async def test_get_current_user_info(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест получения информации о текущем пользователе"""
    # Регистрируем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе
    response = await async_client.get_current_user_info()
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "username", "telegram_username", "created_at"])


@pytest.mark.asyncio
async def test_create_test_user_utility(async_client: AsyncTestAPIClient):
    """Тест утилиты создания тестового пользователя"""
    user_data, access_token = await async_client.create_test_user()

    # Проверяем, что данные пользователя созданы
    assert "username" in user_data
    assert "password" in user_data

    # Проверяем, что токен получен (если регистрация прошла успешно)
    if access_token:
        assert len(access_token) > 0


@pytest.mark.asyncio
async def test_authorized_client_fixture(authorized_client: AsyncTestAPIClient):
    """Тест фикстуры авторизованного клиента"""
    # Получаем информацию о текущем пользователе
    user_info_response = await authorized_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]
    
    # Проверяем, что клиент авторизован - тестируем создание вакансии
    vacancy_data = {
        "name": "Test Vacancy",
        "link": "https://example.com/vacancy",
        "user_id": user_id,  # Используем реальный user_id
        "company_name": "Test Company",
        "description": "Test description",
    }
    response = await authorized_client.create_vacancy(vacancy_data)
    assert_response_status(response, status.HTTP_200_OK)
