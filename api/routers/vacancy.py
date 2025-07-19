import logging
from typing import List

from core.dependencies import get_vacancy_service
from core.exceptions import UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Path, status
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
    try:
        return await vacancy_service.create_vacancy(vacancy_data)
    except UserNotFoundError as e:
        logger.error(f"Пользователь не найден: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Ошибка создания вакансии: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания вакансии",
        )


@router.get("/get_vacancy/{vacancy_id}", response_model=VacancySchema)
async def get_vacancy(
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Получение вакансии по ID"""
    try:
        vacancy = await vacancy_service.get_vacancy_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вакансия не найдена",
            )
        return vacancy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения вакансии: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения вакансии",
        )


@router.get("/get_vacancies/{username}", response_model=List[VacancySchema])
async def get_vacancies(
    username: str = Path(..., description="Username пользователя"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Получение вакансий пользователя по username"""
    try:
        return await vacancy_service.get_vacancies_by_username(username)
    except Exception as e:
        logger.error(f"Ошибка получения вакансий: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения вакансий",
        )


@router.put("/update_vacancy/{vacancy_id}", response_model=VacancySchema)
async def update_vacancy(
    vacancy_data: VacancyUpdateSchema,
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Обновление вакансии"""
    try:
        updated_vacancy = await vacancy_service.update_vacancy(vacancy_id, vacancy_data)
        if not updated_vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вакансия не найдена",
            )
        return updated_vacancy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления вакансии: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления вакансии",
        )


@router.delete("/delete_vacancy/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: int = Path(..., description="ID вакансии"),
    vacancy_service: VacancyService = Depends(get_vacancy_service),
):
    """Удаление вакансии"""
    try:
        success = await vacancy_service.delete_vacancy(vacancy_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вакансия не найдена",
            )
        return {"message": "Вакансия успешно удалена"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления вакансии: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления вакансии",
        )
