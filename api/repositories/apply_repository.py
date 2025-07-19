from typing import List, Optional

from models import ApplyModel
from schemas.apply import ApplyCreateSchema, ApplyUpdateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ApplyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, apply_data: ApplyCreateSchema) -> ApplyModel:
        """Создает новый отклик"""
        apply = ApplyModel(
            id=ApplyModel.generate_id(apply_data.user_id, apply_data.name),
            user_id=apply_data.user_id,
            name=apply_data.name,
            link=apply_data.link,
            company_name=apply_data.company_name,
            description=apply_data.description,
        )
        self.db.add(apply)
        await self.db.commit()
        await self.db.refresh(apply)
        return apply

    async def get_by_id(self, apply_id: str) -> Optional[ApplyModel]:
        """Получает отклик по ID"""
        result = await self.db.execute(
            select(ApplyModel).where(ApplyModel.id == apply_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> List[ApplyModel]:
        """Получает все отклики пользователя"""
        result = await self.db.execute(
            select(ApplyModel).where(ApplyModel.user_id == user_id)
        )
        return result.scalars().all()

    async def update(
        self, apply_id: str, apply_data: ApplyUpdateSchema
    ) -> Optional[ApplyModel]:
        """Обновляет отклик"""
        apply = await self.get_by_id(apply_id)
        if not apply:
            return None

        # Обновляем только переданные поля
        if apply_data.name is not None:
            apply.name = apply_data.name
        if apply_data.link is not None:
            apply.link = apply_data.link
        if apply_data.company_name is not None:
            apply.company_name = apply_data.company_name
        if apply_data.description is not None:
            apply.description = apply_data.description

        await self.db.commit()
        await self.db.refresh(apply)
        return apply

    async def delete(self, apply_id: str) -> bool:
        """Удаляет отклик"""
        apply = await self.get_by_id(apply_id)
        if not apply:
            return False

        await self.db.delete(apply)
        await self.db.commit()
        return True
