import logging
import os

from config import app_config
from core.exception_handlers import register_exception_handlers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import admin, auth, stage, templates, vacancy

# Настройка логирования
logging.basicConfig(
    level=app_config.LOG_LEVEL,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)

app = FastAPI(
    title="Applyr API",
    description="API для управления вакансиями и этапами",
    version="1.0.0",
)

# Регистрация обработчиков исключений
register_exception_handlers(app)

# Подключение статики
app.mount(
    "/static",
    StaticFiles(directory="static" if os.path.isdir("static") else "api/static"),
    name="static",
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(vacancy.router)
app.include_router(stage.router)
app.include_router(templates.router)
app.include_router(admin.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
