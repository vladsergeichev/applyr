import logging

from exceptions import TokenInvalidException, UserNotFoundException
from fastapi import Depends
from fastapi.security import HTTPBearer
from models import UserModel
from repositories.auth_repository import AuthRepository
from repositories.stage_repository import StageRepository
from repositories.vacancy_repository import VacancyRepository
from services.admin_service import AdminService
from services.auth_service import AuthService
from services.stage_service import StageService
from services.vacancy_service import VacancyService
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import verify_token
from database import get_async_db

security = HTTPBearer()
logger = logging.getLogger(__name__)


async def get_current_user(token=Depends(security)) -> UserModel:
    """Получение текущего пользователя из токена"""
    try:
        payload = verify_token(token.credentials)
        if not payload or payload.get("type") != "access":
            raise TokenInvalidException()

        user_id = payload.get("user_id")
        username = payload.get("username")
        telegram_username = payload.get("telegram_username")

        if not user_id or not username:
            raise TokenInvalidException()

        # Создаем объект пользователя из данных токена
        user = UserModel(
            id=user_id,
            username=username,
            telegram_username=telegram_username,
        )

        return user

    except (TokenInvalidException, UserNotFoundException):
        raise
    except Exception as e:
        logger.error(f"Ошибка получения пользователя: {e}")
        raise TokenInvalidException()


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


def get_admin_service(
    auth_repo: AuthRepository = Depends(get_auth_repository),
    vacancy_repo: VacancyRepository = Depends(get_vacancy_repository),
    stage_repo: StageRepository = Depends(get_stage_repository),
) -> AdminService:
    """Создает сервис администратора"""
    return AdminService(auth_repo, vacancy_repo, stage_repo)
