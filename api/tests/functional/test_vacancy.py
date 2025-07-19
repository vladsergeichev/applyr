import pytest
from fastapi import status

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import (
    assert_response_contains,
    assert_response_has_error,
    assert_response_status,
)
from tests.factories.base_factories import VacancyFactory, UserFactory


@pytest.mark.asyncio
async def test_create_vacancy_success(
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного создания вакансии"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе для получения ID
    user_info_response = await async_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]

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
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного получения вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе для получения ID
    user_info_response = await async_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]

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
async def test_get_vacancies_by_username_success(
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного получения вакансий пользователя"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе для получения ID
    user_info_response = await async_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]

    # Создаем несколько вакансий
    for _ in range(3):
        vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
        create_response = await async_client.create_vacancy(vacancy_data)
        assert_response_status(create_response, status.HTTP_200_OK)

    # Получаем вакансии пользователя
    response = await async_client.get_vacancies_by_username(user_data["username"])
    assert_response_status(response, status.HTTP_200_OK)
    
    # Проверяем, что получили список
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_vacancies_by_username_not_found(async_client: AsyncTestAPIClient):
    """Тест получения вакансий несуществующего пользователя"""
    response = await async_client.get_vacancies_by_username("nonexistent_user")
    assert_response_status(response, status.HTTP_200_OK)
    
    # Должен вернуться пустой список
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_update_vacancy_success(
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного обновления вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе для получения ID
    user_info_response = await async_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]

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
    async_client: AsyncTestAPIClient, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного удаления вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем токен для авторизации
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)

    # Получаем информацию о пользователе для получения ID
    user_info_response = await async_client.get_current_user_info()
    assert_response_status(user_info_response, status.HTTP_200_OK)
    user_info = user_info_response.json()
    user_id = user_info["id"]

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