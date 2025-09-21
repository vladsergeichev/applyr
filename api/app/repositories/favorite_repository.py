from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FavoriteModel


class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_vacancy_and_user(
        self, vacancy_id: int, user_id: int
    ) -> FavoriteModel | None:
        """Получает запись избранного по ID вакансии и пользователя"""
        result = await self.db.execute(
            select(FavoriteModel).where(
                FavoriteModel.vacancy_id == vacancy_id,
                FavoriteModel.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self, vacancy_id: int, user_id: int, notes: str | None
    ) -> FavoriteModel:
        """Создает или обновляет запись в избранном"""
        favorite = await self.get_by_vacancy_and_user(vacancy_id, user_id)

        if favorite:
            favorite.notes = notes
        else:
            favorite = FavoriteModel(
                vacancy_id=vacancy_id,
                user_id=user_id,
                notes=notes,
            )
            self.db.add(favorite)

        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite
