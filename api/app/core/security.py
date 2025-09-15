from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import app_config

# Настройки хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширует пароль"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создает access токен"""
    to_encode = data.copy()
    to_encode["type"] = "access"  # обязательно указываем тип
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=app_config.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, app_config.secret_key, algorithm=app_config.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Создает refresh токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=app_config.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, app_config.secret_key, algorithm=app_config.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """Проверяет токен и возвращает данные"""
    try:
        payload = jwt.decode(
            token, app_config.secret_key, algorithms=[app_config.algorithm]
        )
        return payload
    except JWTError:
        return None


def get_token_hash(token: str) -> str:
    """Создает хеш токена для хранения в БД"""
    return pwd_context.hash(token)
