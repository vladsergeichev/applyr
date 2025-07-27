from typing import List, Optional

from models import VacancyModel
from schemas.vacancy import VacancyCreateSchema, VacancyUpdateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class VacancyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, vacancy_data: VacancyCreateSchema) -> VacancyModel:
        """Создает новую вакансию"""
        vacancy = VacancyModel(
            user_id=vacancy_data.user_id,
            name=vacancy_data.name,
            link=vacancy_data.link,
            company_name=vacancy_data.company_name,
            description=vacancy_data.description,
        )
        self.db.add(vacancy)
        await self.db.commit()
        await self.db.refresh(vacancy)
        return vacancy

    async def get_by_id(self, vacancy_id: int) -> Optional[VacancyModel]:
        """Получает вакансию по ID"""
        result = await self.db.execute(
            select(VacancyModel).where(VacancyModel.id == vacancy_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[VacancyModel]:
        """Получает все вакансии пользователя"""
        result = await self.db.execute(
            select(VacancyModel).where(VacancyModel.user_id == user_id).order_by(VacancyModel.created_at.desc())
        )
        return result.scalars().all()

    async def get_all(self) -> List[VacancyModel]:
        """Получает все вакансии"""
        result = await self.db.execute(select(VacancyModel))
        return result.scalars().all()

    async def update(
        self, vacancy_id: int, vacancy_data: VacancyUpdateSchema
    ) -> Optional[VacancyModel]:
        """Обновляет вакансию"""
        vacancy = await self.get_by_id(vacancy_id)
        if not vacancy:
            return None

        # Обновляем только переданные поля
        if vacancy_data.name is not None:
            vacancy.name = vacancy_data.name
        if vacancy_data.link is not None:
            vacancy.link = vacancy_data.link
        if vacancy_data.company_name is not None:
            vacancy.company_name = vacancy_data.company_name
        if vacancy_data.description is not None:
            vacancy.description = vacancy_data.description

        await self.db.commit()
        await self.db.refresh(vacancy)
        return vacancy

    async def delete(self, vacancy_id: int) -> bool:
        """Удаляет вакансию"""
        vacancy = await self.get_by_id(vacancy_id)
        if not vacancy:
            return False

        await self.db.delete(vacancy)
        await self.db.commit()
        return True
