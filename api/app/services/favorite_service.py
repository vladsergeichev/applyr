import logging

from app.repositories.favorite_repository import FavoriteRepository

logger = logging.getLogger(__name__)


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository):
        self.favorite_repository = favorite_repository

    async def get_notes(self, vacancy_id: int, user_id: int) -> str | None:
        """Сохраняет заметки к вакансии"""
        favorite = await self.favorite_repository.get_by_vacancy_and_user(
            vacancy_id, user_id
        )
        if favorite is None:
            return None
        return favorite.notes

    async def update_notes(
        self, vacancy_id: int, user_id: int, notes: str | None
    ) -> str:
        """Сохраняет заметки к вакансии"""
        favorite = await self.favorite_repository.create_or_update(
            vacancy_id, user_id, notes
        )
        return favorite.notes
