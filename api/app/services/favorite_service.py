import logging

from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.favorite import FavoriteBaseSchema

logger = logging.getLogger(__name__)


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository):
        self.favorite_repository = favorite_repository

    async def get_favorite(self, vacancy_id: int, user_id: int) -> FavoriteBaseSchema:
        """Возвращает заметки к вакансии"""
        favorite = await self.favorite_repository.get_by_vacancy_and_user(
            vacancy_id, user_id
        )
        if favorite is None:
            return FavoriteBaseSchema()
        return FavoriteBaseSchema.model_validate(favorite)

    async def update_favorite(
        self, vacancy_id: int, user_id: int, favorite_data: FavoriteBaseSchema
    ) -> FavoriteBaseSchema:
        """Обновляет заметки к вакансии"""
        favorite = await self.favorite_repository.create_or_update(
            vacancy_id, user_id, favorite_data
        )
        return FavoriteBaseSchema.model_validate(favorite)
