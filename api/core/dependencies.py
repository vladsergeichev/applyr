import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from models import UserModel
from repositories.auth_repository import AuthRepository
from repositories.stage_repository import StageRepository
from repositories.vacancy_repository import VacancyRepository
from services.auth_service import AuthService
from services.stage_service import StageService
from services.vacancy_service import VacancyService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.exceptions import (
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    UserAlreadyExistsError,
)
from core.security import verify_token
from database import get_async_db

security = HTTPBearer()
logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(security), db: AsyncSession = Depends(get_async_db)
) -> UserModel:
    """Получение текущего пользователя из токена"""
    try:
        payload = verify_token(token.credentials)
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
            )

        user_id = payload.get("user_id")
        result = await db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден",
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации",
        )


def get_auth_repository(db: AsyncSession = Depends(get_async_db)) -> AuthRepository:
    """Создает репозиторий пользователей"""
    return AuthRepository(db)


def get_vacancy_repository(
    db: AsyncSession = Depends(get_async_db),
) -> VacancyRepository:
    """Создает репозиторий вакансий"""
    return VacancyRepository(db)


def get_stage_repository(db: AsyncSession = Depends(get_async_db)) -> StageRepository:
    """Создает репозиторий этапов"""
    return StageRepository(db)


def get_auth_service(
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    """Создает сервис аутентификации"""
    return AuthService(auth_repo)


def get_vacancy_service(
    vacancy_repo: VacancyRepository = Depends(get_vacancy_repository),
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> VacancyService:
    """Создает сервис вакансий"""
    return VacancyService(vacancy_repo, auth_repo)


def get_stage_service(
    stage_repo: StageRepository = Depends(get_stage_repository),
    vacancy_repo: VacancyRepository = Depends(get_vacancy_repository),
) -> StageService:
    """Создает сервис этапов"""
    return StageService(stage_repo, vacancy_repo)
