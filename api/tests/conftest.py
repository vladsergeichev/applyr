import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_async_db
from main import app


# Тестовая база данных
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5433/test_db"


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для тестов"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Создает тестовый engine для БД"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Очищаем БД после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Создает тестовую сессию БД"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        # Очищаем данные после каждого теста
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest.fixture
async def client(test_session):
    """Создает тестовый клиент"""
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_async_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


# Фикстуры для тестовых данных
@pytest.fixture
def test_user_data():
    """Тестовые данные пользователя"""
    return {
        "id": 123456789,
        "name": "Test User",
        "username": "testuser"
    }


@pytest.fixture
def test_apply_data():
    """Тестовые данные отклика"""
    return {
        "user_id": 123456789,
        "name": "Python Developer",
        "link": "https://example.com/job",
        "company_name": "Test Company",
        "description": "Test job description"
    }


@pytest.fixture
def test_state_data():
    """Тестовые данные состояния"""
    return {
        "name": "Applied"
    }


@pytest.fixture
def test_auth_data():
    """Тестовые данные для аутентификации"""
    return {
        "username": "testuser",
        "password": "testpass123",
        "name": "Test User"
    } 