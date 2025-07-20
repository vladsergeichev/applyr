import os

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Конфигурация проекта"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Логирование
    LOG_LEVEL: str = "INFO"

    # База данных
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 10

    # Network
    HTTP_ONLY: bool = True          # True означает, что cookie не доступны через JavaScript
    SECURE_COOKIES: bool = True     # True означает, что cookie передаются только по HTTPS
    SAME_SITE_COOKIES: str = "lax"  # none/lax/strict
    DOMAIN: str = "127.0.0.1"       # Домен для установки cookie, например, "example.com"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


app_config = AppConfig()

# Подключение шаблонов
templates = Jinja2Templates(
    directory="static/templates"
    if os.path.isdir("static/templates")
    else "api/static/templates"
)
