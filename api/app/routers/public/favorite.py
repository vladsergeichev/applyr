import logging

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_favorite_service
from app.models import UserModel
from app.schemas.favorite import FavoriteBaseSchema
from app.services.favorite_service import FavoriteService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorite", tags=["favorite"])


@router.put("/{vacancy_id}")
async def update_favorite(
    vacancy_id: int,
    favorite_data: FavoriteBaseSchema,
    favorite_service: FavoriteService = Depends(get_favorite_service),
    current_user: UserModel = Depends(get_current_user),
) -> FavoriteBaseSchema:
    """Обновляет заметки к вакансии"""
    return await favorite_service.update_favorite(
        vacancy_id, current_user.id, favorite_data
    )
