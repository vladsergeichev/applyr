from config import app_config
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://applyr_user:applyr_password@localhost:5432/applyr")

# Используем переменные окружения напрямую для избежания циклического импорта
DB_USER = os.getenv("DB_USER", "applyr_user")
DB_PASS = os.getenv("DB_PASS", "applyr_password")
DB_NAME = os.getenv("DB_NAME", "applyr")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
