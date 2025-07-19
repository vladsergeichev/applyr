import logging

from core.exceptions import (
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    UserAlreadyExistsError,
)
from core.security import create_access_token, create_refresh_token, verify_token
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from schemas.auth import AuthResultSchema

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepository, auth_repo: AuthRepository):
        self.user_repo = user_repo
        self.auth_repo = auth_repo

    async def register(
        self, username: str, password: str, name: str
    ) -> AuthResultSchema:
        """Регистрация нового пользователя"""
        # Проверяем, существует ли пользователь
        existing_user = await self.user_repo.get_by_username(username)
        if existing_user:
            raise UserAlreadyExistsError(
                f"Пользователь с username '{username}' уже существует"
            )

        # Создаем пользователя
        user = await self.user_repo.create(username, password, name)

        # Создаем токены
        tokens = await self._create_tokens(user)

        logger.info(f"Зарегистрирован пользователь: {username}")
        return AuthResultSchema(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_id=user.id,
            username=user.username,
        )

    async def login(self, username: str, password: str) -> AuthResultSchema:
        """Вход пользователя"""
        # Проверяем учетные данные
        user = await self.user_repo.get_user_with_password_check(username, password)
        if not user:
            raise InvalidCredentialsError("Неверный username или пароль")

        # Создаем токены
        tokens = await self._create_tokens(user)

        logger.info(f"Пользователь вошел в систему: {username}")
        return AuthResultSchema(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_id=user.id,
            username=user.username,
        )

    async def refresh_access_token(self, refresh_token: str) -> str:
        """Обновляет access токен"""
        # Проверяем refresh токен
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise TokenInvalidError("Недействительный refresh токен")

        user_id = payload.get("user_id")
        username = payload.get("username")

        if not user_id or not username:
            raise TokenInvalidError("Недействительный refresh токен")

        # Проверяем, существует ли токен в БД
        db_token = await self.auth_repo.get_valid_refresh_token(user_id)
        if not db_token:
            raise TokenExpiredError("Refresh токен истек или недействителен")

        # Создаем новый access токен
        access_token = create_access_token(
            data={"user_id": user_id, "username": username}
        )

        logger.info(f"Обновлен токен для пользователя: {username}")
        return access_token

    async def logout(self, refresh_token: str) -> bool:
        """Выход пользователя"""
        # Проверяем токен
        payload = verify_token(refresh_token)
        if payload:
            user_id = payload.get("user_id")
            if user_id:
                # Удаляем токен из БД
                await self.auth_repo.delete_refresh_token(user_id)

        logger.info("Пользователь вышел из системы")
        return True

    async def _create_tokens(self, user) -> dict:
        """Создает access и refresh токены"""
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id, "username": user.username}
        )

        # Сохраняем refresh токен в БД
        await self.auth_repo.save_refresh_token(user.id, refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}
