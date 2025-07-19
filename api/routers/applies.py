import logging
from typing import List

from core.dependencies import get_apply_service
from fastapi import APIRouter, Depends, HTTPException, Path, status
from schemas.apply import ApplyCreateSchema, ApplySchema, ApplyUpdateSchema
from services.apply_service import ApplyService

router = APIRouter(prefix="/applies", tags=["applies"])
logger = logging.getLogger(__name__)


@router.post("/create_apply", response_model=ApplySchema)
async def create_apply(
    apply_data: ApplyCreateSchema,
    apply_service: ApplyService = Depends(get_apply_service),
):
    """Создание нового отклика"""
    try:
        return await apply_service.create_apply(apply_data)
    except Exception as e:
        logger.error(f"Ошибка создания отклика: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания отклика",
        )


@router.get("/get_applies/{username}", response_model=List[ApplySchema])
async def get_applies(
    username: str = Path(..., description="Username пользователя"),
    apply_service: ApplyService = Depends(get_apply_service),
):
    """Получение откликов пользователя по username"""
    try:
        return await apply_service.get_applies_by_username(username)
    except Exception as e:
        logger.error(f"Ошибка получения откликов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения откликов",
        )


@router.put("/update_apply/{apply_id}", response_model=ApplySchema)
async def update_apply(
    apply_data: ApplyUpdateSchema,
    apply_id: str = Path(..., description="ID отклика"),
    apply_service: ApplyService = Depends(get_apply_service),
):
    """Обновление отклика"""
    try:
        updated_apply = await apply_service.update_apply(apply_id, apply_data)
        if not updated_apply:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отклик не найден",
            )
        return updated_apply
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления отклика: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления отклика",
        )


@router.delete("/delete_apply/{apply_id}")
async def delete_apply(
    apply_id: str = Path(..., description="ID отклика"),
    apply_service: ApplyService = Depends(get_apply_service),
):
    """Удаление отклика"""
    try:
        success = await apply_service.delete_apply(apply_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Отклик не найден",
            )
        return {"message": "Отклик успешно удален"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления отклика: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления отклика",
        )
