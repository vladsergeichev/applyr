from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Общая конфигурация проекта"""

    name: str = "applyr_api"
    description: str = "Сервис отслеживания вакансий"
    version: str = "0.0.1"

    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    api_url: str

    telegram_bot_token: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


app_config = AppConfig()
