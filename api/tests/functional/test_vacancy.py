import pytest
from fastapi import status

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import (
    assert_response_contains,
    assert_response_status,
)
from tests.factories.base_factories import UserFactory, VacancyFactory


@pytest.mark.asyncio
async def test_create_vacancy_success(
    async_client: AsyncTestAPIClient,
    vacancy_factory: VacancyFactory,
    user_factory: UserFactory,
):
    """Тест успешного создания вакансии"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем user_id из токена
    user_id = async_client.get_user_id_from_token(access_token)

    # Создаем вакансию
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "link", "user_id", "created_at"])


@pytest.mark.asyncio
async def test_create_vacancy_invalid_data(
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory
):
    """Тест создания вакансии с невалидными данными"""
    invalid_data = {
        "user_id": 1,
        "name": "",  # Пустое название
        "link": "invalid-url",  # Невалидная ссылка
    }
    response = await async_client.create_vacancy(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)


@pytest.mark.asyncio
async def test_get_vacancy_success(
    async_client: AsyncTestAPIClient,
    vacancy_factory: VacancyFactory,
    user_factory: UserFactory,
):
    """Тест успешного получения вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем user_id из токена
    user_id = async_client.get_user_id_from_token(access_token)

    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    vacancy_id = create_response.json()["id"]

    # Получаем вакансию
    response = await async_client.get_vacancy(vacancy_id)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "link", "user_id"])


@pytest.mark.asyncio
async def test_get_vacancy_not_found(async_client: AsyncTestAPIClient):
    """Тест получения несуществующей вакансии"""
    response = await async_client.get_vacancy(999)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_get_vacancies_success(
    async_client: AsyncTestAPIClient,
    vacancy_factory: VacancyFactory,
    user_factory: UserFactory,
):
    """Тест успешного получения вакансий текущего пользователя"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем user_id из токена
    user_id = async_client.get_user_id_from_token(access_token)

    # Создаем несколько вакансий
    for _ in range(3):
        vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
        create_response = await async_client.create_vacancy(vacancy_data)
        assert_response_status(create_response, status.HTTP_200_OK)

    # Получаем вакансии текущего пользователя
    response = await async_client.get_vacancies()
    assert_response_status(response, status.HTTP_200_OK)

    # Проверяем, что получили список
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3  # Должно быть 3 вакансии


@pytest.mark.asyncio
async def test_get_vacancies_empty_for_new_user(
    async_client: AsyncTestAPIClient,
    user_factory: UserFactory,
):
    """Тест получения вакансий для нового пользователя (должен вернуть пустой список)"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем вакансии нового пользователя (должен быть пустой список)
    response = await async_client.get_vacancies()
    assert_response_status(response, status.HTTP_200_OK)

    # Проверяем, что получили пустой список
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # У нового пользователя нет вакансий


@pytest.mark.asyncio
async def test_get_vacancies_unauthorized(async_client: AsyncTestAPIClient):
    """Тест получения вакансий без авторизации (должен вернуть 403 Forbidden)"""
    # Создаем новый клиент без авторизации
    from app.main import app
    from tests.common.api_client import AsyncTestAPIClient

    # Создаем новый клиент без авторизации
    unauth_client = AsyncTestAPIClient.build_app_client(app)

    response = await unauth_client.get_vacancies()
    assert_response_status(response, status.HTTP_403_FORBIDDEN)


@pytest.mark.asyncio
async def test_update_vacancy_success(
    async_client: AsyncTestAPIClient,
    vacancy_factory: VacancyFactory,
    user_factory: UserFactory,
):
    """Тест успешного обновления вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем user_id из токена
    user_id = async_client.get_user_id_from_token(access_token)

    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    vacancy_id = create_response.json()["id"]

    # Обновляем вакансию
    update_data = vacancy_factory.build_vacancy_update_data()
    response = await async_client.update_vacancy(vacancy_id, update_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "link", "updated_at"])


@pytest.mark.asyncio
async def test_update_vacancy_not_found(
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory
):
    """Тест обновления несуществующей вакансии"""
    update_data = vacancy_factory.build_vacancy_update_data()
    response = await async_client.update_vacancy(999, update_data)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_delete_vacancy_success(
    async_client: AsyncTestAPIClient,
    vacancy_factory: VacancyFactory,
    user_factory: UserFactory,
):
    """Тест успешного удаления вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем user_id из токена
    user_id = async_client.get_user_id_from_token(access_token)

    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    vacancy_id = create_response.json()["id"]

    # Удаляем вакансию
    response = await async_client.delete_vacancy(vacancy_id)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["message"])


@pytest.mark.asyncio
async def test_delete_vacancy_not_found(async_client: AsyncTestAPIClient):
    """Тест удаления несуществующей вакансии"""
    response = await async_client.delete_vacancy(999)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_vacancy_validation_errors(async_client: AsyncTestAPIClient):
    """Тест валидации данных вакансии"""
    # Тест с пустым названием
    invalid_data = {
        "name": "",
        "link": "https://example.com",
        "user_id": 1,
    }
    response = await async_client.create_vacancy(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Тест с неверной ссылкой
    invalid_data = {
        "name": "Test Vacancy",
        "link": "invalid-url",
        "user_id": 1,
    }
    response = await async_client.create_vacancy(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Тест с отрицательным user_id
    invalid_data = {
        "name": "Test Vacancy",
        "link": "https://example.com",
        "user_id": -1,
    }
    response = await async_client.create_vacancy(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
