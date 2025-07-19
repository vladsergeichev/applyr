from typing import Optional

from core.security import get_password_hash, verify_password
from models import UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Получает пользователя по ID"""
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        """Получает пользователя по username"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, username: str, password: str, name: str) -> UserModel:
        """Создает нового пользователя"""
        password_hash = get_password_hash(password)
        user = UserModel(
            username=username,
            name=name,
            password_hash=password_hash,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def verify_password(self, username: str, password: str) -> bool:
        """Проверяет пароль пользователя"""
        user = await self.get_by_username(username)
        if not user or not user.password_hash:
            return False
        return verify_password(password, user.password_hash)

    async def get_user_with_password_check(
        self, username: str, password: str
    ) -> Optional[UserModel]:
        """Получает пользователя с проверкой пароля"""
        user = await self.get_by_username(username)
        if not user or not user.password_hash:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    async def create_with_id(
        self, user_id: int, name: str, username: Optional[str] = None
    ) -> UserModel:
        """Создает пользователя с указанным ID (для Telegram)"""
        user = UserModel(
            id=user_id,
            username=username,
            name=name,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: UserModel) -> UserModel:
        """Обновляет пользователя"""
        await self.db.commit()
        await self.db.refresh(user)
        return user
