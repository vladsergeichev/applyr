import pytest
from fastapi import status

from tests.common.api_client import AsyncTestAPIClient
from tests.common.utils import assert_response_contains, assert_response_status
from tests.factories.base_factories import ApplyFactory


@pytest.mark.asyncio
async def test_create_apply_success(
    async_client: AsyncTestAPIClient, apply_factory: ApplyFactory
):
    """Тест успешного создания отклика"""
    apply_data = apply_factory.build_apply_data()
    response = await async_client.create_apply(apply_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "link", "user_id", "created_at"])


@pytest.mark.asyncio
async def test_create_apply_invalid_data(async_client: AsyncTestAPIClient):
    """Тест создания отклика с неверными данными"""
    # Сначала создаем пользователя
    import uuid

    user_data = {
        "username": f"testuser_invalid_{uuid.uuid4().hex[:8]}",
        "password": "password123",
        "name": "Test User",
    }
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Получаем ID пользователя из токена
    # token_data = register_response.json()
    # Декодируем токен, чтобы получить user_id (в реальном проекте нужно добавить утилиту)
    # Пока используем ID 1, который должен существовать после регистрации

    invalid_apply_data = {
        "name": "",  # Пустое имя
        "link": "not-a-url",  # Неверный URL
        "user_id": 1,  # Используем существующий ID
    }
    response = await async_client.create_apply(invalid_apply_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)


@pytest.mark.asyncio
async def test_create_apply_missing_required_fields(async_client: AsyncTestAPIClient):
    """Тест создания отклика без обязательных полей"""
    incomplete_apply_data = {
        "name": "Test Job",
        # Отсутствует link и user_id
    }
    response = await async_client.create_apply(incomplete_apply_data)
    assert_response_status(response, status.HTTP_422_UNPROCESSABLE_ENTITY)


@pytest.mark.asyncio
async def test_get_applies_by_username_success(
    async_client: AsyncTestAPIClient, user_factory
):
    """Тест получения откликов пользователя по username"""
    # Сначала создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Создаем отклик для этого пользователя
    apply_data = {
        "name": "Test Job",
        "link": "https://example.com/job",
        "user_id": 1,
        "company_name": "Test Company",
        "description": "Test description",
    }
    create_response = await async_client.create_apply(apply_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    # Получаем отклики пользователя
    response = await async_client.get(f"/applies/get_applies/{user_data['username']}")
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "link", "user_id"])


@pytest.mark.asyncio
async def test_get_applies_by_username_not_found(async_client: AsyncTestAPIClient):
    """Тест получения откликов несуществующего пользователя"""
    response = await async_client.get("/applies/get_applies/nonexistent_user")
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_update_apply_success(
    async_client: AsyncTestAPIClient, apply_factory: ApplyFactory
):
    """Тест успешного обновления отклика"""
    # Сначала создаем пользователя
    import uuid

    user_data = {
        "username": f"testuser_update_{uuid.uuid4().hex[:8]}",
        "password": "password123",
        "name": "Test User",
    }
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Создаем отклик
    apply_data = apply_factory.build_apply_data()
    apply_data["user_id"] = 1  # Используем ID первого пользователя
    create_response = await async_client.create_apply(apply_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    created_apply = create_response.json()
    apply_id = created_apply["id"]

    # Обновляем отклик
    update_data = {"name": "Updated Job Title", "description": "Updated description"}
    response = await async_client.update_apply(apply_id, update_data)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["id", "name", "description"])

    # Проверяем, что данные обновились
    updated_apply = response.json()
    assert updated_apply["name"] == "Updated Job Title"
    assert updated_apply["description"] == "Updated description"


@pytest.mark.asyncio
async def test_update_apply_not_found(async_client: AsyncTestAPIClient):
    """Тест обновления несуществующего отклика"""
    update_data = {"name": "Updated Job Title", "description": "Updated description"}
    response = await async_client.update_apply("nonexistent-id", update_data)
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_delete_apply_success(
    async_client: AsyncTestAPIClient, apply_factory: ApplyFactory
):
    """Тест успешного удаления отклика"""
    # Сначала создаем пользователя
    import uuid

    user_data = {
        "username": f"testuser_delete_{uuid.uuid4().hex[:8]}",
        "password": "password123",
        "name": "Test User",
    }
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Создаем отклик
    apply_data = apply_factory.build_apply_data()
    apply_data["user_id"] = 1  # Используем ID первого пользователя
    create_response = await async_client.create_apply(apply_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    created_apply = create_response.json()
    apply_id = created_apply["id"]

    # Удаляем отклик
    response = await async_client.delete_apply(apply_id)
    assert_response_status(response, status.HTTP_200_OK)
    assert_response_contains(response, ["message"])


@pytest.mark.asyncio
async def test_delete_apply_not_found(async_client: AsyncTestAPIClient):
    """Тест удаления несуществующего отклика"""
    response = await async_client.delete_apply("nonexistent-id")
    assert_response_status(response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_apply_crud_workflow(
    async_client: AsyncTestAPIClient, apply_factory: ApplyFactory
):
    """Тест полного цикла CRUD операций с откликом"""
    # Сначала создаем пользователя
    import uuid

    user_data = {
        "username": f"testuser_crud_{uuid.uuid4().hex[:8]}",
        "password": "password123",
        "name": "Test User",
    }
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # 1. Создание
    apply_data = apply_factory.build_apply_data()
    apply_data["user_id"] = 1  # Используем ID первого пользователя
    create_response = await async_client.create_apply(apply_data)
    assert_response_status(create_response, status.HTTP_200_OK)

    created_apply = create_response.json()
    apply_id = created_apply["id"]
    print(f"Created apply with ID: {apply_id}")

    # 2. Чтение
    get_response = await async_client.get_apply(apply_id)
    print(f"Get response status: {get_response.status_code}")
    print(f"Get response body: {get_response.text}")
    assert_response_status(get_response, status.HTTP_200_OK)
    assert get_response.json()["id"] == apply_id

    # 3. Обновление
    update_data = {"name": "Updated Job Title", "company_name": "Updated Company"}
    update_response = await async_client.update_apply(apply_id, update_data)
    assert_response_status(update_response, status.HTTP_200_OK)

    # 4. Удаление
    delete_response = await async_client.delete_apply(apply_id)
    assert_response_status(delete_response, status.HTTP_200_OK)

    # 5. Проверяем, что отклик удален
    get_deleted_response = await async_client.get_apply(apply_id)
    assert_response_status(get_deleted_response, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_create_multiple_applies_for_user(
    async_client: AsyncTestAPIClient, user_factory, apply_factory: ApplyFactory
):
    """Тест создания нескольких откликов для одного пользователя"""
    # Создаем пользователя
    user_data = user_factory.build_user_data()
    register_response = await async_client.register_user(user_data)
    assert_response_status(register_response, status.HTTP_200_OK)

    # Создаем несколько откликов
    applies_count = 3
    for i in range(applies_count):
        apply_data = apply_factory.build_apply_data()
        apply_data["name"] = f"Job {i+1}"
        response = await async_client.create_apply(apply_data)
        assert_response_status(response, status.HTTP_200_OK)

    # Получаем все отклики пользователя
    response = await async_client.get(f"/applies/get_applies/{user_data['username']}")
    assert_response_status(response, status.HTTP_200_OK)

    applies = response.json()
    assert len(applies) >= applies_count
