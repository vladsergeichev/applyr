from datetime import datetime, timedelta
from typing import Optional

from core.security import get_token_hash
from models import RefreshTokenModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_refresh_token(
        self, user_id: int, refresh_token: str
    ) -> RefreshTokenModel:
        """Сохраняет refresh токен в БД"""
        token_hash = get_token_hash(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=10)

        refresh_token_model = RefreshTokenModel(
            id=RefreshTokenModel.generate_id(user_id),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.db.add(refresh_token_model)
        await self.db.commit()
        await self.db.refresh(refresh_token_model)
        return refresh_token_model

    async def get_valid_refresh_token(
        self, user_id: int
    ) -> Optional[RefreshTokenModel]:
        """Получает действительный refresh токен пользователя"""
        result = await self.db.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.expires_at > datetime.utcnow(),
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
            select(RefreshTokenModel).where(
                RefreshTokenModel.expires_at <= datetime.utcnow()
            )
        )
        expired_tokens = result.scalars().all()

        for token in expired_tokens:
            await self.db.delete(token)

        await self.db.commit()
        return len(expired_tokens)
