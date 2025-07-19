import logging
from typing import List, Optional

from core.exceptions import UserNotFoundError
from repositories.apply_repository import ApplyRepository
from repositories.user_repository import UserRepository
from schemas.apply import ApplyCreateSchema, ApplySchema, ApplyUpdateSchema

logger = logging.getLogger(__name__)


class ApplyService:
    def __init__(self, apply_repo: ApplyRepository, user_repo: UserRepository):
        self.apply_repo = apply_repo
        self.user_repo = user_repo

    async def create_apply(self, apply_data: ApplyCreateSchema) -> ApplySchema:
        """Создает новый отклик"""
        # Проверяем, существует ли пользователь
        user = await self.user_repo.get_by_id(apply_data.user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {apply_data.user_id} не найден")

        apply = await self.apply_repo.create(apply_data)
        logger.info(f"Создан отклик {apply.id} для пользователя {apply_data.user_id}")
        return apply

    async def get_applies_by_username(self, username: str) -> List[ApplySchema]:
        """Получает отклики пользователя по username"""
        user = await self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"Пользователь с username '{username}' не найден")
            return []

        applies = await self.apply_repo.get_by_user_id(user.id)
        logger.info(f"Получено {len(applies)} откликов для пользователя @{username}")
        return applies

    async def update_apply(
        self, apply_id: str, apply_data: ApplyUpdateSchema
    ) -> Optional[ApplySchema]:
        """Обновляет отклик"""
        apply = await self.apply_repo.get_by_id(apply_id)
        if not apply:
            return None

        updated_apply = await self.apply_repo.update(apply_id, apply_data)
        logger.info(f"Обновлен отклик {apply_id}")
        return updated_apply

    async def delete_apply(self, apply_id: str) -> bool:
        """Удаляет отклик"""
        apply = await self.apply_repo.get_by_id(apply_id)
        if not apply:
            return False

        await self.apply_repo.delete(apply_id)
        logger.info(f"Удален отклик {apply_id}")
        return True
