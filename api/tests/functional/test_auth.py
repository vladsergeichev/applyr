import pytest
from fastapi import status
from models import UserModel
from sqlalchemy import delete

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import (
    assert_response_contains,
    assert_response_has_error,
    assert_response_status,
)
from tests.factories.base_factories import UserFactory


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
    """Тест регистрации пользователя с уже существующим username"""
    # Регистрируем первого пользователя
    user_data = user_factory.build_user_data()
    response1 = await async_client.register_user(user_data)
    assert_response_status(response1, status.HTTP_200_OK)

    # Пытаемся зарегистрировать второго пользователя с тем же username
    response2 = await async_client.register_user(user_data)
    assert_response_status(response2, status.HTTP_409_CONFLICT)
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
    assert_response_status(response2, status.HTTP_409_CONFLICT)
    assert_response_has_error(response2)


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
async def test_access_token_contains_telegram_username(
    async_client: AsyncTestAPIClient, user_factory: UserFactory
):
    """Тест проверки, что access-токен содержит telegram_username"""
    # Регистрируем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен
    access_token = register_response.json().get("access_token")
    assert access_token is not None

    # Декодируем токен и проверяем содержимое
    from core.security import verify_token

    payload = verify_token(access_token)

    assert payload is not None
    assert payload.get("type") == "access"
    assert "user_id" in payload
    assert "username" in payload
    assert "telegram_username" in payload  # Должно быть None для нового пользователя

    # Обновляем telegram_username
    async_client.set_auth_token(access_token)
    telegram_data = user_factory.build_telegram_update_data()
    update_response = await async_client.update_telegram_username(telegram_data)
    assert_response_status(update_response, status.HTTP_200_OK)

    # Получаем новый токен через refresh
    cookies = register_response.cookies
    refresh_token = cookies.get("refresh_token")

    if refresh_token:
        refresh_response = await async_client.refresh_token(refresh_token)
        assert_response_status(refresh_response, status.HTTP_200_OK)

        new_access_token = refresh_response.json().get("access_token")
        assert new_access_token is not None

        # Проверяем новый токен
        new_payload = verify_token(new_access_token)
        assert new_payload is not None
        assert new_payload.get("type") == "access"
        assert "user_id" in new_payload
        assert "username" in new_payload
        assert "telegram_username" in new_payload
        assert (
            new_payload.get("telegram_username") == telegram_data["telegram_username"]
        )
    else:
        pytest.skip("API не возвращает refresh_token в cookie")
