from config import app_config
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# URL для подключения
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{app_config.DB_USER}:{app_config.DB_PASS}@{app_config.DB_HOST}:{app_config.DB_PORT}/{app_config.DB_NAME}"
SYNC_DATABASE_URL = f"postgresql://{app_config.DB_USER}:{app_config.DB_PASS}@{app_config.DB_HOST}:{app_config.DB_PORT}/{app_config.DB_NAME}"

# Синхронный engine для Alembic
engine = create_engine(SYNC_DATABASE_URL)

# Асинхронный engine для FastAPI
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=app_config.LOG_LEVEL == "DEBUG",
    pool_pre_ping=True,
    pool_recycle=3600,
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_db():
    """Асинхронная функция для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
