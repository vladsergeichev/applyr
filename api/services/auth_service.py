import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_token_hash,
    verify_password,
    verify_token,
)
from models import RefreshModel, UserModel
from repositories.auth_repository import AuthRepository
from schemas.auth import AuthLoginSchema, AuthRegisterSchema, AuthResponseSchema

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def register_user(
        self, user_data: AuthRegisterSchema, db: AsyncSession
    ) -> Tuple[AuthResponseSchema, str]:
        """Регистрация нового пользователя"""
        # Проверяем, существует ли пользователь с таким username
        existing_user = await self.auth_repo.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким username уже существует",
            )

        # Создаем нового пользователя
        db_user = UserModel(
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        # Создаем токены
        access_token, refresh_token = self._create_tokens(db_user)
        await self._save_refresh_token(db_user.id, refresh_token, db)

        logger.info(f"Зарегистрирован пользователь: {user_data.username}")
        return AuthResponseSchema(access_token=access_token), refresh_token

    async def login_user(
        self, user_data: AuthLoginSchema, db: AsyncSession
    ) -> Tuple[AuthResponseSchema, str]:
        """Вход пользователя"""
        # Ищем пользователя
        user = await self.auth_repo.get_by_username(user_data.username)

        if not user or not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный username или пароль",
            )

        # Проверяем пароль
        if not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный username или пароль",
            )

        # Создаем токены
        access_token, refresh_token = self._create_tokens(user)
        await self._save_refresh_token(user.id, refresh_token, db)

        logger.info(f"Пользователь вошел в систему: {user.username}")
        return AuthResponseSchema(access_token=access_token), refresh_token

    async def refresh_access_token(
        self, refresh_token: str, db: AsyncSession
    ) -> AuthResponseSchema:
        """Обновление access токена"""
        # Проверяем refresh токен
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный refresh токен",
            )

        user_id = payload.get("user_id")
        username = payload.get("username")

        # Проверяем, существует ли токен в БД
        result = await db.execute(
            select(RefreshModel).where(
                RefreshModel.user_id == user_id,
                RefreshModel.expires_at > datetime.utcnow(),
            )
        )
        db_token = result.scalar_one_or_none()

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh токен недействителен",
            )

        # Создаем новый access токен
        access_token = create_access_token(
            data={"user_id": user_id, "username": username}
        )

        logger.info(f"Обновлен токен для пользователя: {username}")
        return AuthResponseSchema(access_token=access_token)

    async def logout_user(
        self, refresh_token: Optional[str], db: AsyncSession
    ) -> None:
        """Выход пользователя"""
        if refresh_token:
            # Проверяем токен
            payload = verify_token(refresh_token)
            if payload:
                user_id = payload.get("user_id")
                # Удаляем токен из БД
                result = await db.execute(
                    select(RefreshModel).where(
                        RefreshModel.user_id == user_id,
                        RefreshModel.expires_at > datetime.utcnow(),
                    )
                )
                db_token = result.scalar_one_or_none()
                if db_token:
                    await db.delete(db_token)
                    await db.commit()

    async def update_telegram_username(
        self, user_id: int, telegram_username: str, db: AsyncSession
    ) -> None:
        """Обновление Telegram username"""
        # Проверяем, не занят ли telegram_username другим пользователем
        existing_user = await self.auth_repo.get_by_telegram_username(telegram_username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Telegram username уже используется",
            )

        await self.auth_repo.update_telegram_username(user_id, telegram_username, db)
        logger.info(f"Обновлен Telegram username для пользователя {user_id}")

    def _create_tokens(self, user: UserModel) -> Tuple[str, str]:
        """Создает access и refresh токены для пользователя"""
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id, "username": user.username}
        )
        return access_token, refresh_token

    async def _save_refresh_token(
        self, user_id: int, refresh_token: str, db: AsyncSession
    ) -> None:
        """Сохраняет refresh токен в БД"""
        token_hash = get_token_hash(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=10)

        db_refresh_token = RefreshModel(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(db_refresh_token)
        await db.commit()

    def _set_refresh_cookie(self, refresh_token: str, response: Optional[Response]) -> None:
        """Устанавливает refresh токен в cookie"""
        if response:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,  # True для HTTPS
                samesite="lax",
                max_age=10 * 24 * 60 * 60,  # 10 дней
            )

    def _delete_refresh_cookie(self, response: Response) -> None:
        """Удаляет refresh токен из cookie"""
        response.delete_cookie(key="refresh_token")
