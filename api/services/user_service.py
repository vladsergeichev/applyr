import logging
from typing import Optional

from repositories.user_repository import UserRepository
from schemas.user import UserSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(
        self, user_id: int, name: str, username: Optional[str] = None
    ) -> UserSchema:
        """Создает или обновляет пользователя"""
        # Проверяем, существует ли пользователь
        existing_user = await self.user_repo.get_by_id(user_id)

        if existing_user:
            # Обновляем username если он изменился
            if username and existing_user.username != username:
                existing_user.username = username
                await self.user_repo.update(existing_user)
            return existing_user

        # Создаем нового пользователя
        user = await self.user_repo.create_with_id(user_id, name, username)

        logger.info(f"Создан пользователь {user_id}: {name} (@{username})")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        """Получает пользователя по ID"""
        return await self.user_repo.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        """Получает пользователя по username"""
        return await self.user_repo.get_by_username(username)
