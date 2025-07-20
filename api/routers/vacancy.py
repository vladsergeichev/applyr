import logging
from typing import List

from core.dependencies import get_current_user, get_vacancy_service
from fastapi import APIRouter, Depends, Path
from models import UserModel
from schemas.vacancy import VacancyCreateSchema, VacancySchema, VacancyUpdateSchema
from services.vacancy_service import VacancyService

router = APIRouter(prefix="/vacancy", tags=["vacancy"])
logger = logging.getLogger(__name__)


@router.post("/create_vacancy", response_model=VacancySchema)
async def create_vacancy(
    vacancy_data: VacancyCreateSchema,
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Создание новой вакансии"""
    return await vacancy_service.create_vacancy(vacancy_data)


@router.get("/get_vacancy/{vacancy_id}", response_model=VacancySchema)
async def get_vacancy(
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Получение вакансии по ID"""
    return await vacancy_service.get_vacancy_by_id(vacancy_id)


@router.get("/get_vacancies", response_model=List[VacancySchema])
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
