import logging
from typing import List

from core.dependencies import get_stage_service
from fastapi import APIRouter, Depends, Path
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
    return await stage_service.create_stage(stage_data)


@router.get("/get_stage/{stage_id}", response_model=StageSchema)
async def get_stage(
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Получение этапа по ID"""
    return await stage_service.get_stage_by_id(stage_id)


@router.get("/get_stages/{vacancy_id}", response_model=List[StageSchema])
async def get_stages(
    vacancy_id: int = Path(..., description="ID вакансии"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Получение этапов вакансии"""
    return await stage_service.get_stages_by_vacancy_id(vacancy_id)


@router.put("/update_stage/{stage_id}", response_model=StageSchema)
async def update_stage(
    stage_data: StageUpdateSchema,
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Обновление этапа"""
    return await stage_service.update_stage(stage_id, stage_data)


@router.delete("/delete_stage/{stage_id}")
async def delete_stage(
    stage_id: int = Path(..., description="ID этапа"),
    stage_service: StageService = Depends(get_stage_service),
):
    """Удаление этапа"""
    await stage_service.delete_stage(stage_id)
    return {"message": "Этап успешно удален"}
