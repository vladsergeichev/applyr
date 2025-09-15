from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import VacancyModel
from app.schemas.stage import GetStageSchema
from app.schemas.vacancy import (
    GetVacancySchema,
    VacancyCreateSchema,
    VacancyUpdateSchema,
    VacancyBaseSchema,
)


class VacancyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, vacancy_data: VacancyBaseSchema) -> VacancyModel:
        """Создает новую вакансию"""
        vacancy = VacancyModel(**vacancy_data.model_dump())
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

    async def get_by_user_id(self, user_id: int) -> list[GetVacancySchema]:
        """Получает все вакансии пользователя с этапами"""
        query = (
            select(VacancyModel)
            .options(joinedload(VacancyModel.stages))
            .where(VacancyModel.user_id == user_id)
            .order_by(VacancyModel.created_at.desc())
        )
        result = await self.db.execute(query)
        vacancies = result.unique().scalars().all()  # Убираем дубли с помощью unique()

        return [
            GetVacancySchema(
                id=vacancy.id,
                user_id=vacancy.user_id,
                name=vacancy.name,
                link=vacancy.link,
                company_name=vacancy.company_name,
                description=vacancy.description,
                salary=vacancy.salary,
                experience=vacancy.experience,
                location=vacancy.location,
                employment=vacancy.employment,
                requirements=vacancy.requirements,
                conditions=vacancy.conditions,
                created_at=vacancy.created_at,
                updated_at=vacancy.updated_at,
                stages=[
                    GetStageSchema(
                        id=stage.id,
                        stage_type=stage.stage_type.value,
                        title=stage.title,
                        description=stage.description,
                        created_at=stage.created_at,
                        updated_at=stage.updated_at,
                    )
                    for stage in vacancy.stages
                ],
            )
            for vacancy in vacancies
        ]

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
