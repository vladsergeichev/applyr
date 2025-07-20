import pytest

from tests.common.api_client import AsyncTestAPIClient
from tests.factories.base_factories import UserFactory


class TestAdminEndpoints:
    """Тесты для админских эндпоинтов"""

    @pytest.mark.asyncio
    async def test_get_users_success(self, async_client: AsyncTestAPIClient):
        """Тест получения всех пользователей"""
        # Создаем тестовых пользователей через API
        user_factory = UserFactory()
        user1_data = user_factory.build_user_data()
        user2_data = user_factory.build_user_data()

        await async_client.register_user(user1_data)
        await async_client.register_user(user2_data)

        response = await async_client.get("/admin/get_users")

        assert response.status_code == 200
        users = response.json()

        assert len(users) >= 2
        usernames = [user["username"] for user in users]
        assert user1_data["username"] in usernames
        assert user2_data["username"] in usernames

        # Проверяем структуру ответа
        user = users[0]
        assert "id" in user
        assert "username" in user
        assert "telegram_username" in user
        assert "created_at" in user

    @pytest.mark.asyncio
    async def test_get_vacancies_success(self, async_client: AsyncTestAPIClient):
        """Тест получения всех вакансий"""
        # Создаем тестового пользователя и вакансии через API
        user_factory = UserFactory()
        user_data = user_factory.build_user_data()

        # Регистрируем пользователя
        register_response = await async_client.register_user(user_data)
        assert register_response.status_code == 200

        # Получаем токен и информацию о пользователе
        access_token = register_response.json().get("access_token")
        async_client.set_auth_token(access_token)

        # Получаем user_id из токена
        user_id = async_client.get_user_id_from_token(access_token)

        # Создаем вакансии
        vacancy1_data = {
            "name": "Test Vacancy 1",
            "description": "Test description 1",
            "link": "https://example.com/1",
            "company_name": "Test Company 1",
            "user_id": user_id,
        }
        vacancy2_data = {
            "name": "Test Vacancy 2",
            "description": "Test description 2",
            "link": "https://example.com/2",
            "company_name": "Test Company 2",
            "user_id": user_id,
        }

        await async_client.create_vacancy(vacancy1_data)
        await async_client.create_vacancy(vacancy2_data)

        response = await async_client.get("/admin/get_vacancies")

        assert response.status_code == 200
        vacancies = response.json()

        assert len(vacancies) >= 2
        vacancy_names = [vacancy["name"] for vacancy in vacancies]
        assert "Test Vacancy 1" in vacancy_names
        assert "Test Vacancy 2" in vacancy_names

        # Проверяем структуру ответа
        vacancy = vacancies[0]
        assert "id" in vacancy
        assert "name" in vacancy
        assert "description" in vacancy
        assert "link" in vacancy
        assert "company_name" in vacancy
        assert "user_id" in vacancy
        assert "created_at" in vacancy

    @pytest.mark.asyncio
    async def test_get_stages_success(self, async_client: AsyncTestAPIClient):
        """Тест получения всех этапов"""
        # Создаем тестового пользователя, вакансию и этапы через API
        user_factory = UserFactory()
        user_data = user_factory.build_user_data()

        # Регистрируем пользователя
        register_response = await async_client.register_user(user_data)
        assert register_response.status_code == 200

        # Получаем токен и информацию о пользователе
        access_token = register_response.json().get("access_token")
        async_client.set_auth_token(access_token)

        # Получаем user_id из токена
        user_id = async_client.get_user_id_from_token(access_token)

        # Создаем вакансию
        vacancy_data = {
            "name": "Test Vacancy",
            "description": "Test description",
            "link": "https://example.com",
            "company_name": "Test Company",
            "user_id": user_id,
        }
        vacancy_response = await async_client.create_vacancy(vacancy_data)
        assert vacancy_response.status_code == 200

        # Получаем ID созданной вакансии
        vacancy_id = vacancy_response.json().get("id", 1)

        # Создаем этапы
        stage1_data = {
            "stage_type": "Test Stage 1",
            "description": "Test stage description 1",
            "vacancy_id": vacancy_id,
        }
        stage2_data = {
            "stage_type": "Test Stage 2",
            "description": "Test stage description 2",
            "vacancy_id": vacancy_id,
        }

        await async_client.create_stage(stage1_data)
        await async_client.create_stage(stage2_data)

        response = await async_client.get("/admin/get_stages")

        assert response.status_code == 200
        stages = response.json()

        assert len(stages) >= 2
        stage_names = [stage["name"] for stage in stages]
        assert "Test Stage 1" in stage_names
        assert "Test Stage 2" in stage_names

        # Проверяем структуру ответа
        stage = stages[0]
        assert "id" in stage
        assert "name" in stage
        assert "description" in stage
        assert "vacancy_id" in stage
        assert "created_at" in stage

    @pytest.mark.asyncio
    async def test_get_tokens_success(self, async_client: AsyncTestAPIClient):
        """Тест получения всех токенов"""
        response = await async_client.get("/admin/get_tokens")

        assert response.status_code == 200
        tokens = response.json()

        # Проверяем структуру ответа
        if tokens:  # Если есть токены
            token = tokens[0]
            assert "id" in token
            assert "token_hash" in token
            assert "user_id" in token
            assert "expires_at" in token
            assert "created_at" in token
