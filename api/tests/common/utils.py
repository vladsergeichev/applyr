import uuid
from typing import Any, Dict

from faker import Faker


def generate_test_uuid() -> str:
    """Генерирует UUID для тестов"""
    return str(uuid.uuid4())


def generate_test_username(faker: Faker) -> str:
    """Генерирует тестовое имя пользователя"""
    return f"testuser_{faker.uuid4().hex[:8]}"


def generate_test_password(faker: Faker, length: int = 12) -> str:
    """Генерирует тестовый пароль"""
    return faker.password(length=length)


def generate_test_telegram_username(faker: Faker) -> str:
    """Генерирует тестовый Telegram username"""
    return f"@{faker.user_name()}"


def create_test_user_data(faker: Faker, **overrides) -> Dict[str, Any]:
    """Создает тестовые данные пользователя"""
    data = {
        "username": generate_test_username(faker),
        "password": generate_test_password(faker),
    }
    data.update(overrides)
    return data


def create_test_vacancy_data(faker: Faker, **overrides) -> Dict[str, Any]:
    """Создает тестовые данные вакансии"""
    data = {
        "name": faker.job(),
        "link": faker.url(),
        "user_id": 1,
        "company_name": faker.company(),
        "description": faker.text(max_nb_chars=200),
    }
    data.update(overrides)
    return data


def create_test_stage_data(faker: Faker, **overrides) -> Dict[str, Any]:
    """Создает тестовые данные этапа"""
    data = {
        "vacancy_id": 1,
        "stage_type": faker.random_element(
            [
                "Отклик отправлен",
                "Резюме просмотрено",
                "Приглашение на собеседование",
                "Собеседование пройдено",
                "Тестовое задание",
                "Оффер",
                "Отказ",
            ]
        ),
        "description": faker.text(max_nb_chars=200),
    }
    data.update(overrides)
    return data


def assert_response_status(response: Any, expected_status: int) -> None:
    """Проверяет статус ответа"""
    assert (
        response.status_code == expected_status
    ), f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"


def assert_response_contains(response: Any, expected_keys: list[str]) -> None:
    """Проверяет наличие ключей в JSON ответе"""
    try:
        data = response.json()
        for key in expected_keys:
            assert key in data, f"Key '{key}' not found in response: {data}"
    except ValueError:
        assert False, f"Response is not JSON: {response.text}"


def assert_response_has_error(
    response: Any, expected_error_type: str | None = None
) -> None:
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
