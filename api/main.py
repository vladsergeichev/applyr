import logging
import os

from config import app_config
from core.exception_handlers import register_exception_handlers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.all import admin_router, internal_router, public_router

# Настройка логирования
logging.basicConfig(
    level=app_config.LOG_LEVEL,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)

app = FastAPI(
    title="Applyr API",
    description="API для управления вакансиями",
    version="1.0.0",
)

# Регистрация обработчиков исключений
register_exception_handlers(app)

# Подключение статики
# app.mount(
#     "/",
#     StaticFiles(
#         directory="static" if os.path.isdir("static") else "api/static",
#         html=True),
#     name="static",
# )

# Подключение роутеров
app.include_router(admin_router, prefix="/api")
app.include_router(internal_router, prefix="/api")
app.include_router(public_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
