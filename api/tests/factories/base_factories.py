from collections.abc import Callable
from datetime import datetime
from typing import Any

from faker import Faker


class BaseModelFactory:
    """Базовая фабрика для создания тестовых данных с использованием Faker"""

    __faker__ = Faker(locale=["ru_RU", "en_US"])

    @classmethod
    def get_provider_map(cls) -> dict[Any, Callable[[], Any]]:
        """Возвращает карту провайдеров для различных типов данных"""
        return {
            str: cls.__faker__.pystr,
            int: cls.__faker__.random_int,
            float: cls.__faker__.pyfloat,
            bool: cls.__faker__.boolean,
            datetime: cls.__faker__.date_time,
            list: cls.__faker__.pylist,
            dict: cls.__faker__.pydict,
        }

    @classmethod
    def build(cls, **overrides) -> dict[str, Any]:
        """Создает словарь с тестовыми данными"""
        # Базовые данные будут определены в наследниках
        data = {}

        # Применяем переопределения
        data.update(overrides)

        return data


class UserFactory(BaseModelFactory):
    """Фабрика для создания тестовых данных пользователей"""

    @classmethod
    def build_user_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для регистрации пользователя"""
        import uuid

        data = {
            "username": f"testuser_{uuid.uuid4().hex[:8]}",
            "password": cls.__faker__.password(length=12),
        }
        data.update(overrides)
        return data

    @classmethod
    def build_login_data(
        cls, username: str | None = None, password: str | None = None, **overrides
    ) -> dict[str, Any]:
        """Создает данные для входа пользователя"""
        import uuid

        data = {
            "username": username or f"testuser_{uuid.uuid4().hex[:8]}",
            "password": password or cls.__faker__.password(length=12),
        }
        data.update(overrides)
        return data

    @classmethod
    def build_telegram_update_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для обновления Telegram username"""
        data = {
            "telegram_username": f"@{cls.__faker__.user_name()}",
        }
        data.update(overrides)
        return data

    @classmethod
    def build_token_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные токена"""
        data = {
            "access_token": cls.__faker__.uuid4(),
            "refresh_token": cls.__faker__.uuid4(),
            "token_type": "bearer",
        }
        data.update(overrides)
        return data


class VacancyFactory(BaseModelFactory):
    """Фабрика для создания тестовых данных вакансий"""

    @classmethod
    def build_vacancy_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для создания вакансии"""
        data = {
            "name": cls.__faker__.job(),
            "link": cls.__faker__.url(),
            "company_name": cls.__faker__.company(),
            "description": cls.__faker__.text(max_nb_chars=200),
        }
        data.update(overrides)
        return data

    @classmethod
    def build_vacancy_update_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для обновления вакансии"""
        data = {
            "name": cls.__faker__.job(),
            "link": cls.__faker__.url(),
            "company_name": cls.__faker__.company(),
            "description": cls.__faker__.text(max_nb_chars=200),
        }
        data.update(overrides)
        return data


class StageFactory(BaseModelFactory):
    """Фабрика для создания тестовых данных этапов"""

    @classmethod
    def build_stage_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для создания этапа"""
        data = {
            "state_type": cls.__faker__.random_element([
                "Отклик отправлен",
                "Резюме просмотрено", 
                "Приглашение на собеседование",
                "Собеседование пройдено",
                "Тестовое задание",
                "Оффер",
                "Отказ"
            ]),
            "description": cls.__faker__.text(max_nb_chars=200),
            "occurred_at": cls.__faker__.date_time().isoformat(),
        }
        data.update(overrides)
        return data

    @classmethod
    def build_stage_update_data(cls, **overrides) -> dict[str, Any]:
        """Создает данные для обновления этапа"""
        data = {
            "state_type": cls.__faker__.random_element([
                "Отклик отправлен",
                "Резюме просмотрено", 
                "Приглашение на собеседование",
                "Собеседование пройдено",
                "Тестовое задание",
                "Оффер",
                "Отказ"
            ]),
            "description": cls.__faker__.text(max_nb_chars=200),
            "occurred_at": cls.__faker__.date_time().isoformat(),
        }
        data.update(overrides)
        return data
