import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_auth_service, get_vacancy_service
from app.schemas.auth import UserInfoSchema
from app.schemas.vacancy import (
    VacancyCreateSchema,
    VacancySchema,
)
from app.services.auth_service import AuthService
from app.services.vacancy_service import VacancyService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/get_by_telegram/{telegram_username}", response_model=UserInfoSchema)
async def get_by_telegram_username(
    telegram_username: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Получить пользователя по telegram_username"""
    user = await auth_service.auth_repo.get_by_telegram_username(telegram_username)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserInfoSchema(
        id=user.id,
        username=user.username,
        telegram_username=user.telegram_username,
        created_at=user.created_at,
    )


@router.post("/create_vacancy", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreateSchema,
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Создание новой вакансии через бот"""
    return await vacancy_service.create_vacancy(vacancy_data)


@router.post("/get_vacancies", response_model=VacancySchema)
async def get_vacancies_by_user_id(
    user_id: int,
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Получение вакансий пользователя по id"""
    return await vacancy_service.get_vacancies_by_user_id(user_id)
