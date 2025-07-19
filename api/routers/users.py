import logging

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_db

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.post("/create_user", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)
):
    """Создание нового пользователя"""
    try:
        # Проверяем, существует ли пользователь
        result = await db.execute(select(models.User).where(models.User.id == user.id))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            # Обновляем username если он изменился
            if user.username and existing_user.username != user.username:
                existing_user.username = user.username
                await db.commit()
                await db.refresh(existing_user)
            return existing_user  # Возвращаем существующего пользователя

        # Создаем нового пользователя
        db_user = models.User(id=user.id, name=user.name, username=user.username)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        logger.info(f"Создан пользователь {user.id}: {user.name} (@{user.username})")
        return db_user

    except Exception as e:
        logger.error(f"Ошибка создания пользователя: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания пользователя",
        )
