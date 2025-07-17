import logging
import os

import models
from fastapi import FastAPI
from routers import applies, states, users, dashboard

from config import app_config
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

# Подключение роутеров
app.include_router(applies.router)
app.include_router(states.router)
app.include_router(users.router)
app.include_router(dashboard.router)


# @app.get("/")
# def read_root():
#     return {"message": "Applyr API работает"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
