import logging
import os

import models
from config import app_config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import applies, dashboard, states, users

from database import engine

# Настройка логирования
logging.basicConfig(
    level=app_config.LOG_LEVEL,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Applyr API",
    description="API для управления откликами на вакансии",
    version="1.0.0",
)

# Подключение статики
app.mount(
    "/static",
    StaticFiles(directory="static" if os.path.isdir("static") else "api/static"),
    name="static",
)

# Подключение шаблонов из config
from config import templates

# Подключение роутеров
app.include_router(applies.router)
app.include_router(states.router)
app.include_router(users.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
