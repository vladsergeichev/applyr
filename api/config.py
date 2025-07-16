from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Конфигурация проекта"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Логирование
    LOG_LEVEL: str = "INFO"

    # База данных
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


app_config = AppConfig()
