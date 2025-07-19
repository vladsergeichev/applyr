from typing import List, Optional

from models import StageModel
from schemas.stage import StageCreateSchema, StageUpdateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class StageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, stage_data: StageCreateSchema) -> StageModel:
        """Создает новый этап"""
        stage = StageModel(
            apply_id=stage_data.apply_id,
            state_type=stage_data.state_type,
            description=stage_data.description,
            occurred_at=stage_data.occurred_at,
        )
        self.db.add(stage)
        await self.db.commit()
        await self.db.refresh(stage)
        return stage

    async def get_by_id(self, stage_id: int) -> Optional[StageModel]:
        """Получает этап по ID"""
        result = await self.db.execute(
            select(StageModel).where(StageModel.id == stage_id)
        )
        return result.scalar_one_or_none()

    async def get_by_vacancy_id(self, vacancy_id: int) -> List[StageModel]:
        """Получает все этапы вакансии"""
        result = await self.db.execute(
            select(StageModel).where(StageModel.apply_id == vacancy_id)
        )
        return result.scalars().all()

    async def update(
        self, stage_id: int, stage_data: StageUpdateSchema
    ) -> Optional[StageModel]:
        """Обновляет этап"""
        stage = await self.get_by_id(stage_id)
        if not stage:
            return None

        # Обновляем только переданные поля
        if stage_data.state_type is not None:
            stage.state_type = stage_data.state_type
        if stage_data.description is not None:
            stage.description = stage_data.description
        if stage_data.occurred_at is not None:
            stage.occurred_at = stage_data.occurred_at

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
