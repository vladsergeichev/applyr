import logging

from fastapi import FastAPI

from app.config import app_config
from app.core.exception_handlers import register_exception_handlers
from app.routers.all import admin_router, internal_router, public_router

# Настройка логирования
logging.basicConfig(
    level=app_config.log_level,
    format=app_config.log_format,
)

app = FastAPI(
    title="Applyr API",
    description="API для управления вакансиями",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Регистрация обработчиков исключений
register_exception_handlers(app)


app.include_router(admin_router, prefix="/api")
app.include_router(internal_router, prefix="/api")
app.include_router(public_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
