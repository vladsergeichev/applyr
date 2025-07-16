from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Конфигурация проекта"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Логирование
    LOG_LEVEL: str = "INFO"
    
    # API
    API_URL: str

    # Telegram
    TELEGRAM_BOT_TOKEN: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


app_config = AppConfig()
