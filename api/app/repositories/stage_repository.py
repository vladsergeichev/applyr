from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StageModel
from app.schemas.stage import StageCreateSchema, StageUpdateSchema


class StageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, stage_data: StageCreateSchema) -> StageModel:
        """Создает новый этап"""
        stage = StageModel(
            vacancy_id=stage_data.vacancy_id,
            stage_type=stage_data.stage_type,
            title=stage_data.title,
            description=stage_data.description,
        )

        # Если передана дата создания, устанавливаем её
        if stage_data.created_at:
            stage.created_at = stage_data.created_at

        self.db.add(stage)
        await self.db.commit()
        await self.db.refresh(stage)
        return stage

    async def get_by_id(self, stage_id: int) -> StageModel | None:
        """Получает этап по ID"""
        result = await self.db.execute(
            select(StageModel).where(StageModel.id == stage_id)
        )
        return result.scalar_one_or_none()

    async def get_by_vacancy_id(self, vacancy_id: int) -> list[StageModel]:
        """Получает все этапы вакансии"""
        result = await self.db.execute(
            select(StageModel).where(StageModel.vacancy_id == vacancy_id)
        )
        return result.scalars().all()

    async def get_all(self) -> list[StageModel]:
        """Получает все этапы"""
        result = await self.db.execute(select(StageModel))
        return result.scalars().all()

    async def update(
        self, stage_id: int, stage_data: StageUpdateSchema
    ) -> StageModel | None:
        """Обновляет этап"""
        stage = await self.get_by_id(stage_id)
        if not stage:
            return None

        # Обновляем только переданные поля
        if stage_data.stage_type is not None:
            stage.stage_type = stage_data.stage_type
        if stage_data.title is not None:
            stage.title = stage_data.title
        if stage_data.description is not None:
            stage.description = stage_data.description

        await self.db.commit()
        await self.db.refresh(stage)
        return stage

    async def delete(self, stage_id: int) -> bool:
        """Удаляет этап"""
        stage = await self.get_by_id(stage_id)
        if not stage:
            return False

        await self.db.delete(stage)
        await self.db.commit()
        return True
