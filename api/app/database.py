from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import app_config

DATABASE_URL = f"postgresql+asyncpg://{app_config.db.url}"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=app_config.log_level == "DEBUG",
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
