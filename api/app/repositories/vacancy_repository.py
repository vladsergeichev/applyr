from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import VacancyModel
from app.schemas.favorite import FavoriteStage
from app.schemas.vacancy import (
    GetVacancySchema,
    VacancyBaseSchema,
    VacancyUpdateSchema,
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

    async def get_by_id(self, vacancy_id: int) -> VacancyModel | None:
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
                contact_link=vacancy.contact_link,
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
            )
            for vacancy in vacancies
        ]

    async def get_all_by_user_id(self, user_id: int) -> list[GetVacancySchema]:
        """Получает все вакансии пользователя с этапами"""
        query = (
            select(VacancyModel)
            .options(joinedload(VacancyModel.favorite))
            .where(VacancyModel.user_id == user_id)
            .order_by(VacancyModel.created_at.desc())
        )
        result = await self.db.execute(query)
        vacancies = result.unique().scalars().all()  # Убираем дубли с помощью unique()
        for vacancy in vacancies:
            if vacancy.favorite:
                vacancy.notes = vacancy.favorite[0].notes
                vacancy.stage = vacancy.favorite[0].stage
            else:
                vacancy.notes = None
                vacancy.stage = FavoriteStage.NOTHING
        return [GetVacancySchema.model_validate(vacancy) for vacancy in vacancies]

    async def get_all(self) -> list[VacancyModel]:
        """Получает все вакансии"""
        result = await self.db.execute(select(VacancyModel))
        return result.scalars().all()

    async def update(
        self, vacancy_id: int, vacancy_data: VacancyUpdateSchema
    ) -> VacancyModel | None:
        """Обновляет вакансию"""
        vacancy = await self.get_by_id(vacancy_id)
        if not vacancy:
            return None

        # Обновляем только переданные поля
        for key, value in vacancy_data.model_dump(exclude_none=True).items():
            setattr(vacancy, key, value)

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
