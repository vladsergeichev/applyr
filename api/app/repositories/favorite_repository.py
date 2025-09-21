from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FavoriteModel
from app.schemas.favorite import FavoriteBaseSchema


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

    async def create(
        self, vacancy_id: int, user_id: int, favorite_data: FavoriteBaseSchema
    ) -> FavoriteModel:
        """Создает запись в избранном"""
        favorite = FavoriteModel(
            vacancy_id=vacancy_id, user_id=user_id, **favorite_data.model_dump()
        )
        self.db.add(favorite)
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite

    async def create_or_update(
        self, vacancy_id: int, user_id: int, favorite_data: FavoriteBaseSchema
    ) -> FavoriteModel:
        """Создает или обновляет запись в избранном"""
        favorite = await self.get_by_vacancy_and_user(vacancy_id, user_id)

        if favorite is None:
            return await self.create(
                vacancy_id=vacancy_id, user_id=user_id, favorite_data=favorite_data
            )

        # Обновляем только переданные поля
        for key, value in favorite_data.model_dump(exclude_none=True).items():
            setattr(favorite, key, value)

        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite
