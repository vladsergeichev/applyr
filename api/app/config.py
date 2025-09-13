from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseModel):
    """Конфигурация PostgreSQL"""

    host: str = "postgres"
    port: str = "5432"
    name: str = "stream_cash"
    user: str = "postgres"
    password: str = "postgres"

    @property
    def url(self) -> str:
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppConfig(BaseSettings):
    """Общая конфигурация проекта"""

    name: str = "applyr_api"
    description: str = "Сервис отслеживания вакансий"
    version: str = "0.0.1"

    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    db: PostgresConfig

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 10

    # Network
    http_only: bool = True  # True означает, что cookie не доступны через JavaScript
    secure_cookies: bool = True  # True означает, что cookie передаются только по HTTPS
    same_site_cookies: str = "lax"  # none/lax/strict
    domain: str = "127.0.0.1"  # Домен для установки cookie, например, "example.com"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


app_config = AppConfig()

# # Подключение шаблонов
# templates = Jinja2Templates(
#     directory="static/templates"
#     if os.path.isdir("static/templates")
#     else "api/static/templates"
# )
