import logging
from datetime import datetime, timedelta

from core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_token_hash,
    verify_password,
    verify_token,
)
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBearer
from models import RefreshModel, UserModel
from schemas.auth import (
    AuthLoginSchema,
    AuthRegisterSchema,
    AuthResponseSchema,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)
security = HTTPBearer()


@router.post("/register", response_model=AuthResponseSchema)
async def register(
    user_data: AuthRegisterSchema,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
):
    """Регистрация нового пользователя"""
    try:
        # Проверяем, существует ли пользователь с таким username
        result = await db.execute(
            select(UserModel).where(UserModel.username == user_data.username)
        )
        existing_user = result.scalar_one_or_none()

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
        access_token = create_access_token(
            data={"user_id": db_user.id, "username": db_user.username}
        )
        refresh_token = create_refresh_token(
            data={"user_id": db_user.id, "username": db_user.username}
        )

        # Сохраняем refresh токен в БД
        token_hash = get_token_hash(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=10)

        db_refresh_token = RefreshModel(
            user_id=db_user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(db_refresh_token)
        await db.commit()

        # Устанавливаем refresh токен в cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # True для HTTPS
            samesite="lax",
            max_age=10 * 24 * 60 * 60,  # 10 дней
        )

        logger.info(f"Зарегистрирован пользователь: {user_data.username}")
        return AuthResponseSchema(access_token=access_token)

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
    db: AsyncSession = Depends(get_async_db),
):
    """Вход пользователя"""
    try:
        # Ищем пользователя
        result = await db.execute(
            select(UserModel).where(UserModel.username == user_data.username)
        )
        user = result.scalar_one_or_none()

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
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id, "username": user.username}
        )

        # Сохраняем refresh токен в БД
        token_hash = get_token_hash(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=10)

        db_refresh_token = RefreshModel(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(db_refresh_token)
        await db.commit()

        # Устанавливаем refresh токен в cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # True для HTTPS
            samesite="lax",
            max_age=10 * 24 * 60 * 60,  # 10 дней
        )

        logger.info(f"Пользователь вошел в систему: {user.username}")
        return AuthResponseSchema(access_token=access_token)

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
async def refresh_token(request: Request, db: AsyncSession = Depends(get_async_db)):
    """Обновление access токена"""
    try:
        # Получаем refresh токен из cookie
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh токен не найден",
            )

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
    request: Request, response: Response, db: AsyncSession = Depends(get_async_db)
):
    """Выход пользователя"""
    try:
        # Получаем refresh токен из cookie
        refresh_token = request.cookies.get("refresh_token")
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

        # Удаляем cookie
        response.delete_cookie(key="refresh_token")

        logger.info("Пользователь вышел из системы")
        return {"message": "Успешный выход"}

    except Exception as e:
        logger.error(f"Ошибка выхода: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка выхода",
        )
