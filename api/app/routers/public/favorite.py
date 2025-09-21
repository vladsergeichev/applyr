import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user, get_favorite_service
from app.exceptions.vacancy_exceptions import VacancyNotFoundException
from app.models import UserModel
from app.schemas.favorite import FavoriteBaseSchema
from app.services.favorite_service import FavoriteService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorite", tags=["favorite"])


@router.post("/{vacancy_id}/update_notes")
async def update_notes(
    vacancy_id: int,
    favorite_data: FavoriteBaseSchema,
    favorite_service: FavoriteService = Depends(get_favorite_service),
    current_user: UserModel = Depends(get_current_user),
) -> dict[str, str]:
    """Сохраняет заметки к вакансии"""
    try:
        notes = await favorite_service.update_notes(
            vacancy_id, current_user.id, favorite_data.notes
        )
        return {"message": "Заметки сохранены", "notes": notes}
    except VacancyNotFoundException:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
