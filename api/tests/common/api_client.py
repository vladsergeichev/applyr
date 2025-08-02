import uuid
from typing import Any, Dict, Optional, Self

from core.security import verify_token
from faker import Faker
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient, Response


class AsyncTestAPIClient(AsyncClient):
    """Асинхронный клиент для тестирования API через HTTP запросы"""

    def __init__(self, app: FastAPI, base_url: str = "http://test"):
        super().__init__(
            base_url=base_url,
            transport=ASGITransport(app),
        )
        self.faker = Faker(locale=["ru_RU", "en_US"])

    @classmethod
    def build_app_client(cls, app: FastAPI, base_url: str = "http://test") -> Self:
        """Создает клиент для тестов с ASGI приложением"""
        return cls(app=app, base_url=base_url)

    @classmethod
    def build_authorized_app_client(
        cls, app: FastAPI, access_token: Optional[str] = None
    ) -> Self:
        """Создает авторизованный клиент для тестов"""
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        client = cls.build_app_client(app=app)
        client.headers.update(headers)
        return client

    def set_auth_token(self, access_token: str):
        """Устанавливает токен авторизации"""
        self.headers["Authorization"] = f"Bearer {access_token}"

    def clear_auth_token(self):
        """Очищает токен авторизации"""
        if "Authorization" in self.headers:
            del self.headers["Authorization"]

    def get_user_id_from_token(self, access_token: str) -> int:
        """Получает user_id из access-токена"""
        payload = verify_token(access_token)
        if payload and "user_id" in payload:
            return payload["user_id"]
        raise ValueError("Invalid access token or missing user_id")

    # Аутентификация
    async def register_user(
        self, user_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """Регистрация пользователя"""
        if user_data is None:
            user_data = {
                "username": f"testuser_{uuid.uuid4().hex[:8]}",
                "password": self.faker.password(length=12),
            }
        return await self.post("/auth/register", json=user_data)

    async def login_user(self, username: str, password: str) -> Response:
        """Вход пользователя"""
        login_data = {"username": username, "password": password}
        return await self.post("/auth/login", json=login_data)

    async def refresh_token(self, refresh_token: str) -> Response:
        """Обновление токена"""
        return await self.post("/auth/refresh", json={"refresh_token": refresh_token})

    async def logout_user(self, refresh_token: str) -> Response:
        """Выход пользователя"""
        return await self.post("/auth/logout", json={"refresh_token": refresh_token})

    async def update_telegram_username(self, telegram_data: Dict[str, Any]) -> Response:
        """Обновление Telegram username"""
        return await self.put("/auth/update_telegram", json=telegram_data)

    # Вакансии
    async def create_vacancy(
        self, vacancy_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """Создание вакансии"""
        if vacancy_data is None:
            vacancy_data = {
                "name": self.faker.job(),
                "link": self.faker.url(),
                "user_id": 1,
                "company_name": self.faker.company(),
                "description": self.faker.text(max_nb_chars=200),
            }
        return await self.post("/api/internal/create_vacancy", json=vacancy_data)

    async def get_vacancy(self, vacancy_id: int) -> Response:
        """Получение конкретной вакансии"""
        return await self.get(f"/vacancy/get_vacancy/{vacancy_id}")

    async def get_vacancies(self) -> Response:
        """Получение вакансий текущего пользователя"""
        return await self.get("/api/internal/get_vacancies")

    async def update_vacancy(
        self, vacancy_id: int, vacancy_data: Dict[str, Any]
    ) -> Response:
        """Обновление вакансии"""
        return await self.put(
            f"/vacancy/update_vacancy/{vacancy_id}", json=vacancy_data
        )

    async def delete_vacancy(self, vacancy_id: int) -> Response:
        """Удаление вакансии"""
        return await self.delete(f"/vacancy/delete_vacancy/{vacancy_id}")

    # Этапы
    async def create_stage(
        self, stage_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """Создание этапа"""
        if stage_data is None:
            stage_data = {
                "vacancy_id": 1,
                "stage_type": "Отклик отправлен",
                "description": self.faker.text(max_nb_chars=200),
                "occurred_at": self.faker.date_time().isoformat(),
            }
        return await self.post("/stage/create_stage", json=stage_data)

    async def get_stage(self, stage_id: int) -> Response:
        """Получение конкретного этапа"""
        return await self.get(f"/stage/get_stage/{stage_id}")

    async def get_stages_by_vacancy_id(self, vacancy_id: int) -> Response:
        """Получение этапов вакансии"""
        return await self.get(f"/stage/get_stages/{vacancy_id}")

    async def update_stage(self, stage_id: int, stage_data: Dict[str, Any]) -> Response:
        """Обновление этапа"""
        return await self.put(f"/stage/update_stage/{stage_id}", json=stage_data)

    async def delete_stage(self, stage_id: int) -> Response:
        """Удаление этапа"""
        return await self.delete(f"/stage/delete_stage/{stage_id}")

    # Утилиты для тестов
    async def create_test_user(self) -> tuple[Dict[str, Any], str]:
        """Создает тестового пользователя и возвращает данные и токен"""
        # Регистрируем пользователя
        user_data = {
            "username": f"testuser_{uuid.uuid4().hex[:8]}",
            "password": self.faker.password(length=12),
        }
        register_response = await self.register_user(user_data)

        if register_response.status_code == status.HTTP_200_OK:
            # Если регистрация успешна, получаем токен
            login_response = await self.login_user(
                user_data["username"], user_data["password"]
            )
            if login_response.status_code == status.HTTP_200_OK:
                token_data = login_response.json()
                return user_data, token_data.get("access_token", "")

        # Если что-то пошло не так, возвращаем данные без токена
        return user_data, ""

    def assert_response_status(self, response: Response, expected_status: int):
        """Проверяет статус ответа"""
        assert (
            response.status_code == expected_status
        ), f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"

    def assert_response_contains(self, response: Response, expected_keys: list[str]):
        """Проверяет наличие ключей в JSON ответе"""
        try:
            data = response.json()
            for key in expected_keys:
                assert key in data, f"Key '{key}' not found in response: {data}"
        except ValueError:
            assert False, f"Response is not JSON: {response.text}"

    def assert_response_has_error(
        self, response: Response, expected_error_type: Optional[str] = None
    ):
        """Проверяет наличие ошибки в ответе"""
        assert (
            response.status_code >= 400
        ), f"Expected error status, got {response.status_code}"
        if expected_error_type:
            try:
                data = response.json()
                assert "detail" in data, f"No 'detail' field in error response: {data}"
            except ValueError:
                assert False, f"Error response is not JSON: {response.text}"
