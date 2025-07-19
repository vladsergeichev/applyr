from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from models import UserModel
from repositories.apply_repository import ApplyRepository
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from services.apply_service import ApplyService
from services.auth_service import AuthService
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    UserAlreadyExistsError,
)
from core.security import verify_token
from database import get_async_db

security = HTTPBearer()


def get_user_repository(db: AsyncSession = Depends(get_async_db)) -> UserRepository:
    """Создает репозиторий пользователей"""
    return UserRepository(db)


def get_auth_repository(db: AsyncSession = Depends(get_async_db)) -> AuthRepository:
    """Создает репозиторий аутентификации"""
    return AuthRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    """Создает сервис аутентификации"""
    return AuthService(user_repo, auth_repo)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Создает сервис пользователей"""
    return UserService(user_repo)


def get_apply_repository(db: AsyncSession = Depends(get_async_db)) -> ApplyRepository:
    """Создает репозиторий откликов"""
    return ApplyRepository(db)


def get_apply_service(
    apply_repo: ApplyRepository = Depends(get_apply_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> ApplyService:
    """Создает сервис откликов"""
    return ApplyService(apply_repo, user_repo)


async def get_current_user(
    token: str = Depends(security), db: AsyncSession = Depends(get_async_db)
) -> UserModel:
    """Получает текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def handle_auth_exceptions(func):
    """Декоратор для обработки исключений аутентификации"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UserAlreadyExistsError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except InvalidCredentialsError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except (TokenInvalidError, TokenExpiredError) as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            )

    return wrapper
