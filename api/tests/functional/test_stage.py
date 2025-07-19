import pytest
from fastapi import status

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import (
    assert_response_contains,
    assert_response_has_error,
    assert_response_status,
)
from tests.factories.base_factories import StageFactory, VacancyFactory, UserFactory


@pytest.mark.asyncio
async def test_create_stage_success(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного создания этапа"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)
    user_info = (await async_client.get_current_user_info()).json()
    user_id = user_info["id"]
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_vacancy_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_vacancy_response, status.HTTP_200_OK)
    vacancy_id = create_vacancy_response.json()["id"]
    # Создаем этап
    stage_data = stage_factory.build_stage_data(apply_id=vacancy_id)
    response = await async_client.create_stage(stage_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "apply_id", "state_type", "created_at"])


@pytest.mark.asyncio
async def test_create_stage_invalid_vacancy_id(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory
):
    """Тест создания этапа с несуществующей вакансией"""
    stage_data = stage_factory.build_stage_data(apply_id=999)
    response = await async_client.create_stage(stage_data)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_get_stage_success(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного получения этапа"""
    # Создаем пользователя, вакансию и этап
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)
    user_info = (await async_client.get_current_user_info()).json()
    user_id = user_info["id"]
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_vacancy_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_vacancy_response, status.HTTP_200_OK)
    vacancy_id = create_vacancy_response.json()["id"]
    stage_data = stage_factory.build_stage_data(apply_id=vacancy_id)
    create_stage_response = await async_client.create_stage(stage_data)
    assert_response_status(create_stage_response, status.HTTP_200_OK)
    stage_id = create_stage_response.json()["id"]
    # Получаем этап
    response = await async_client.get_stage(stage_id)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "apply_id", "state_type"])


@pytest.mark.asyncio
async def test_get_stage_not_found(async_client: AsyncTestAPIClient):
    """Тест получения несуществующего этапа"""
    response = await async_client.get_stage(999)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_get_stages_by_vacancy_id_success(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного получения этапов вакансии"""
    # Создаем пользователя и вакансию
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)
    user_info = (await async_client.get_current_user_info()).json()
    user_id = user_info["id"]
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_vacancy_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_vacancy_response, status.HTTP_200_OK)
    vacancy_id = create_vacancy_response.json()["id"]
    # Создаем несколько этапов
    for _ in range(3):
        stage_data = stage_factory.build_stage_data(apply_id=vacancy_id)
        create_stage_response = await async_client.create_stage(stage_data)
        assert_response_status(create_stage_response, status.HTTP_200_OK)
    # Получаем этапы вакансии
    response = await async_client.get_stages_by_vacancy_id(vacancy_id)
    assert_response_status(response, status.HTTP_200_OK)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_stages_by_vacancy_id_not_found(async_client: AsyncTestAPIClient):
    """Тест получения этапов несуществующей вакансии"""
    response = await async_client.get_stages_by_vacancy_id(999)
    assert_response_status(response, status.HTTP_200_OK)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_update_stage_success(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного обновления этапа"""
    # Создаем пользователя, вакансию и этап
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)
    user_info = (await async_client.get_current_user_info()).json()
    user_id = user_info["id"]
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_vacancy_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_vacancy_response, status.HTTP_200_OK)
    vacancy_id = create_vacancy_response.json()["id"]
    stage_data = stage_factory.build_stage_data(apply_id=vacancy_id)
    create_stage_response = await async_client.create_stage(stage_data)
    assert_response_status(create_stage_response, status.HTTP_200_OK)
    stage_id = create_stage_response.json()["id"]
    # Обновляем этап
    update_data = stage_factory.build_stage_update_data()
    response = await async_client.update_stage(stage_id, update_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "state_type", "updated_at"])


@pytest.mark.asyncio
async def test_update_stage_not_found(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory
):
    """Тест обновления несуществующего этапа"""
    update_data = stage_factory.build_stage_update_data()
    response = await async_client.update_stage(999, update_data)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_delete_stage_success(
    async_client: AsyncTestAPIClient, stage_factory: StageFactory, vacancy_factory: VacancyFactory, user_factory: UserFactory
):
    """Тест успешного удаления этапа"""
    # Создаем пользователя, вакансию и этап
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)
    access_token = register_response.json().get("access_token")
    async_client.set_auth_token(access_token)
    user_info = (await async_client.get_current_user_info()).json()
    user_id = user_info["id"]
    vacancy_data = vacancy_factory.build_vacancy_data(user_id=user_id)
    create_vacancy_response = await async_client.create_vacancy(vacancy_data)
    assert_response_status(create_vacancy_response, status.HTTP_200_OK)
    vacancy_id = create_vacancy_response.json()["id"]
    stage_data = stage_factory.build_stage_data(apply_id=vacancy_id)
    create_stage_response = await async_client.create_stage(stage_data)
    assert_response_status(create_stage_response, status.HTTP_200_OK)
    stage_id = create_stage_response.json()["id"]
    # Удаляем этап
    response = await async_client.delete_stage(stage_id)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["message"])


@pytest.mark.asyncio
async def test_delete_stage_not_found(async_client: AsyncTestAPIClient):
    """Тест удаления несуществующего этапа"""
    response = await async_client.delete_stage(999)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_stage_validation_errors(async_client: AsyncTestAPIClient):
    """Тест валидации данных этапа"""
    # Тест с пустым state_type
    invalid_data = {
        "apply_id": 1,
        "state_type": "",
        "description": "Test description",
        "occurred_at": "2024-01-01T00:00:00",
    }
    response = await async_client.create_stage(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)
    # Тест с отрицательным apply_id
    invalid_data = {
        "apply_id": -1,
        "state_type": "Отклик отправлен",
        "description": "Test description",
        "occurred_at": "2024-01-01T00:00:00",
    }
    response = await async_client.create_stage(invalid_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY) 