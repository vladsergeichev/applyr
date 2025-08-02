import logging

from core.dependencies import get_auth_service, get_current_user
from exceptions import TokenInvalidException
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from models import UserModel
from schemas.auth import (
    AuthLoginSchema,
    AuthRegisterSchema,
    AuthResponseSchema,
    UpdateTelegramSchema,
    UserInfoSchema,
)
from services.auth_service import AuthService

router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)


@router.post("/register", response_model=AuthResponseSchema)
async def register(
    user_data: AuthRegisterSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Регистрация нового пользователя"""
    result, refresh_token = await auth_service.register_user(user_data)
    auth_service.set_refresh_cookie(refresh_token, response)
    return result


@router.post("/login", response_model=AuthResponseSchema)
async def login(
    user_data: AuthLoginSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Вход пользователя"""
    result, refresh_token = await auth_service.login_user(user_data)
    auth_service.set_refresh_cookie(refresh_token, response)
    return result


@router.post("/refresh", response_model=AuthResponseSchema)
async def refresh(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Обновление access токена"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise TokenInvalidException()

    return await auth_service.refresh_access_token(refresh_token)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Выход пользователя"""
    refresh_token = request.cookies.get("refresh_token")
    await auth_service.logout_user(refresh_token)
    auth_service.delete_refresh_cookie(response)
    return {"message": "Успешный выход из системы"}


@router.put("/update_telegram")
async def update_telegram_username(
    telegram_data: UpdateTelegramSchema,
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Обновление Telegram username"""
    await auth_service.update_telegram_username(
        current_user.id, telegram_data.telegram_username
    )
    return {"message": "Telegram username успешно обновлен"}


