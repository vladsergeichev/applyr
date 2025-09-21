import logging

from fastapi import APIRouter, Depends, Path

from app.core.dependencies import (
    get_current_user,
    get_favorite_service,
    get_vacancy_service,
)
from app.models import UserModel
from app.schemas.vacancy import (
    GetVacancySchema,
    VacancyBaseSchema,
    VacancyCreateSchema,
    VacancySchema,
    VacancyUpdateSchema,
)
from app.services.favorite_service import FavoriteService
from app.services.vacancy_service import VacancyService

router = APIRouter(prefix="/vacancy")
logger = logging.getLogger(__name__)


@router.post("/create_vacancy", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyBaseSchema,
    current_user: UserModel = Depends(get_current_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Создание новой вакансии"""
    data = VacancyCreateSchema(user_id=current_user.id, **vacancy_data.model_dump())
    return await vacancy_service.create_vacancy(data)


@router.get("/get_vacancy/{vacancy_id}", response_model=GetVacancySchema)
async def get_vacancy(
    vacancy_id: int = Path(..., description="ID вакансии"),
    current_user: UserModel = Depends(get_current_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
    favorite_service: FavoriteService = Depends(get_favorite_service),
):
    """Получение вакансии по ID"""
    vacancy = await vacancy_service.get_vacancy_by_id(vacancy_id)
    vacancy.notes = await favorite_service.get_notes(vacancy_id, current_user.id)
    return vacancy


@router.get("/get_vacancies", response_model=list[GetVacancySchema])
async def get_vacancies(
    current_user: UserModel = Depends(get_current_user),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Получение вакансий текущего пользователя"""
    return await vacancy_service.get_vacancies_by_user_id(current_user.id)


@router.put("/update_vacancy/{vacancy_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_data: VacancyUpdateSchema,
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Обновление вакансии"""
    return await vacancy_service.update_vacancy(vacancy_id, vacancy_data)


@router.delete("/delete_vacancy/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Удаление вакансии"""
    await vacancy_service.delete_vacancy(vacancy_id)
    return {"message": "Вакансия успешно удалена"}
