import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, get_auth_service
from core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_token_hash,
    verify_password,
    verify_token,
)
from database import get_async_db
from models import UserModel, RefreshModel
from schemas.auth import (
    AuthLoginSchema,
    AuthRegisterSchema,
    AuthResponseSchema,
    UpdateTelegramSchema,
    UserInfoSchema,
)
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=AuthResponseSchema)
async def register(
    user_data: AuthRegisterSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_async_db),
):
    """Регистрация нового пользователя"""
    try:
        result, refresh_token = await auth_service.register_user(user_data, db)
        # Устанавливаем cookie в response
        auth_service._set_refresh_cookie(refresh_token, response)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка регистрации: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка регистрации",
        )


@router.post("/login", response_model=AuthResponseSchema)
async def login(
    user_data: AuthLoginSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_async_db),
):
    """Вход пользователя"""
    try:
        result, refresh_token = await auth_service.login_user(user_data, db)
        # Устанавливаем cookie в response
        auth_service._set_refresh_cookie(refresh_token, response)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка входа: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка входа",
        )


@router.post("/refresh", response_model=AuthResponseSchema)
async def refresh_token(
    request: Request, 
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_async_db)
):
    """Обновление access токена"""
    try:
        # Получаем refresh токен из cookie
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh токен не найден",
            )

        return await auth_service.refresh_access_token(refresh_token, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления токена: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления токена",
        )


@router.post("/logout")
async def logout(
    request: Request, 
    response: Response, 
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_async_db)
):
    """Выход пользователя"""
    try:
        # Получаем refresh токен из cookie
        refresh_token = request.cookies.get("refresh_token")
        
        await auth_service.logout_user(refresh_token, db)
        
        # Удаляем cookie
        auth_service._delete_refresh_cookie(response)
        
        return {"message": "Успешный выход из системы"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка выхода: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка выхода",
        )


@router.put("/update_telegram")
async def update_telegram_username(
    telegram_data: UpdateTelegramSchema,
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_async_db),
):
    """Обновление Telegram username"""
    try:
        await auth_service.update_telegram_username(
            current_user.id, telegram_data.telegram_username, db
        )
        return {"message": "Telegram username успешно обновлен"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления Telegram username: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления Telegram username",
        )


@router.get("/me", response_model=UserInfoSchema)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user),
):
    """Получение информации о текущем пользователе"""
    return current_user
