from datetime import datetime, timedelta
from typing import Optional

from core.security import get_password_hash, get_token_hash, verify_password
from models import RefreshModel, UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Методы для работы с пользователями
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

    async def get_by_telegram_username(
        self, telegram_username: str
    ) -> Optional[UserModel]:
        """Получает пользователя по Telegram username"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.telegram_username == telegram_username)
        )
        return result.scalar_one_or_none()

    async def create(self, username: str, password: str) -> UserModel:
        """Создает нового пользователя"""
        password_hash = get_password_hash(password)
        user = UserModel(
            username=username,
            password_hash=password_hash,
            telegram_username=None,  # telegram_username будет добавлен позже
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
        self, user_id: int, telegram_username: str, username: Optional[str] = None
    ) -> UserModel:
        """Создает пользователя с указанным ID (для Telegram)"""
        user = UserModel(
            id=user_id,
            username=username,
            telegram_username=telegram_username,
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

    # Методы для работы с refresh токенами
    async def save_refresh_token(
        self, user_id: int, refresh_token: str
    ) -> RefreshModel:
        """Сохраняет refresh токен в БД"""
        token_hash = get_token_hash(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=10)

        refresh_token_model = RefreshModel(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.db.add(refresh_token_model)
        await self.db.commit()
        await self.db.refresh(refresh_token_model)
        return refresh_token_model

    async def get_valid_refresh_token(self, user_id: int) -> Optional[RefreshModel]:
        """Получает действительный refresh токен пользователя"""
        result = await self.db.execute(
            select(RefreshModel).where(
                RefreshModel.user_id == user_id,
                RefreshModel.expires_at > datetime.utcnow(),
            )
        )
        return result.scalar_one_or_none()

    async def delete_refresh_token(self, user_id: int) -> bool:
        """Удаляет refresh токен пользователя"""
        token = await self.get_valid_refresh_token(user_id)
        if token:
            await self.db.delete(token)
            await self.db.commit()
            return True
        return False

    async def delete_expired_tokens(self) -> int:
        """Удаляет истекшие токены и возвращает количество удаленных"""
        result = await self.db.execute(
            select(RefreshModel).where(RefreshModel.expires_at <= datetime.utcnow())
        )
        expired_tokens = result.scalars().all()

        for token in expired_tokens:
            await self.db.delete(token)

        await self.db.commit()
        return len(expired_tokens)
