import logging
from typing import List

from core.dependencies import get_stage_service
from core.exceptions import VacancyNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Path, status
from schemas.stage import StageCreateSchema, StageSchema, StageUpdateSchema
from services.stage_service import StageService

router = APIRouter(prefix="/stage", tags=["stage"])
logger = logging.getLogger(__name__)


@router.post("/create_stage", response_model=StageSchema)
async def create_stage(
    stage_data: StageCreateSchema,
    stage_service: StageService = Depends(get_stage_service),
):
    """Создание нового этапа"""
    try:
        return await stage_service.create_stage(stage_data)
    except VacancyNotFoundError as e:
        logger.error(f"Вакансия не найдена: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Ошибка создания этапа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания этапа",
        )


@router.get("/get_stage/{stage_id}", response_model=StageSchema)
async def get_stage(
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Получение этапа по ID"""
    try:
        stage = await stage_service.get_stage_by_id(stage_id)
        if not stage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Этап не найден",
            )
        return stage
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения этапа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения этапа",
        )


@router.get("/get_stages/{vacancy_id}", response_model=List[StageSchema])
async def get_stages(
    vacancy_id: int = Path(..., description="ID вакансии"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Получение этапов вакансии"""
    try:
        return await stage_service.get_stages_by_vacancy_id(vacancy_id)
    except Exception as e:
        logger.error(f"Ошибка получения этапов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения этапов",
        )


@router.put("/update_stage/{stage_id}", response_model=StageSchema)
async def update_stage(
    stage_data: StageUpdateSchema,
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Обновление этапа"""
    try:
        updated_stage = await stage_service.update_stage(stage_id, stage_data)
        if not updated_stage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Этап не найден",
            )
        return updated_stage
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления этапа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления этапа",
        )


@router.delete("/delete_stage/{stage_id}")
async def delete_stage(
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Удаление этапа"""
    try:
        success = await stage_service.delete_stage(stage_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Этап не найден",
            )
        return {"message": "Этап успешно удален"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления этапа: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления этапа",
        )
