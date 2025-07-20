import logging
from typing import Optional, Tuple

from core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from exceptions import (
    InvalidCredentialsException,
    TelegramUsernameAlreadyExistsException,
    TokenExpiredException,
    TokenInvalidException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from fastapi import Response
from models import UserModel
from repositories.auth_repository import AuthRepository
from schemas.auth import AuthLoginSchema, AuthRegisterSchema, AuthResponseSchema

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def register_user(
        self, user_data: AuthRegisterSchema
    ) -> Tuple[AuthResponseSchema, str]:
        """Регистрация нового пользователя"""
        # Проверяем, существует ли пользователь с таким username
        existing_user = await self.auth_repo.get_by_username(user_data.username)
        if existing_user:
            raise UserAlreadyExistsException()

        # Создаем нового пользователя через репозиторий
        db_user = await self.auth_repo.create(user_data.username, user_data.password)

        # Создаем токены
        access_token, refresh_token = AuthService._create_tokens(db_user)
        await self.auth_repo.save_refresh_token(db_user.id, refresh_token)

        logger.info(f"Зарегистрирован пользователь: {user_data.username}")
        return AuthResponseSchema(access_token=access_token), refresh_token

    async def login_user(
        self, user_data: AuthLoginSchema
    ) -> Tuple[AuthResponseSchema, str]:
        """Вход пользователя"""
        # Получаем пользователя с проверкой пароля через репозиторий
        user = await self.auth_repo.get_user_with_password_check(
            user_data.username, user_data.password
        )

        if not user:
            raise InvalidCredentialsException()

        # Создаем токены
        access_token, refresh_token = AuthService._create_tokens(user)
        await self.auth_repo.save_refresh_token(user.id, refresh_token)

        logger.info(f"Пользователь вошел в систему: {user.username}")
        return AuthResponseSchema(access_token=access_token), refresh_token

    async def refresh_access_token(self, refresh_token: str) -> AuthResponseSchema:
        """Обновление access токена"""
        # Проверяем refresh токен
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise TokenInvalidException()

        user_id = payload.get("user_id")
        if not user_id:
            raise TokenInvalidException()

        # Получаем полные данные пользователя из БД через репозиторий
        user = await self.auth_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        # Проверяем, существует ли токен в БД через репозиторий
        db_token = await self.auth_repo.get_valid_refresh_token(user_id)
        if not db_token:
            raise TokenExpiredException()

        # Создаем новый access токен с полными данными пользователя
        access_token_data = {
            "user_id": user.id,
            "username": user.username,
            "telegram_username": user.telegram_username,
        }
        access_token = create_access_token(data=access_token_data)

        logger.info(f"Обновлен токен для пользователя: {user.username}")
        return AuthResponseSchema(access_token=access_token)

    async def logout_user(self, refresh_token: Optional[str]) -> None:
        """Выход пользователя"""
        if refresh_token:
            # Проверяем токен
            payload = verify_token(refresh_token)
            if payload:
                user_id = payload.get("user_id")
                if user_id:
                    # Удаляем токен из БД через репозиторий
                    await self.auth_repo.delete_refresh_token(user_id)

    async def update_telegram_username(
        self, user_id: int, telegram_username: str
    ) -> None:
        """Обновление Telegram username"""
        # Проверяем, не занят ли telegram_username другим пользователем
        existing_user = await self.auth_repo.get_by_telegram_username(telegram_username)
        if existing_user and existing_user.id != user_id:
            raise TelegramUsernameAlreadyExistsException()

        await self.auth_repo.update_telegram_username(user_id, telegram_username)
        logger.info(f"Обновлен Telegram username для пользователя {user_id}")

    @staticmethod
    def _create_tokens(user: UserModel) -> Tuple[str, str]:
        """Создает access и refresh токены для пользователя"""
        # Access токен содержит полную информацию о пользователе
        access_token_data = {
            "user_id": user.id,
            "username": user.username,
            "telegram_username": user.telegram_username,
        }
        access_token = create_access_token(data=access_token_data)

        # Refresh токен содержит только user_id для поиска в БД
        refresh_token = create_refresh_token(data={"user_id": user.id})
        return access_token, refresh_token

    def set_refresh_cookie(
        self, refresh_token: str, response: Optional[Response]
    ) -> None:
        """Устанавливает refresh токен в cookie"""
        if response:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,  # True для HTTPS
                samesite="strict",  # Защита от CSRF атак
                max_age=10 * 24 * 60 * 60,  # 10 дней
            )

    def delete_refresh_cookie(self, response: Response) -> None:
        """Удаляет refresh токен из cookie"""
        response.delete_cookie(key="refresh_token")
