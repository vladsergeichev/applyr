import logging
from typing import List

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_db

router = APIRouter(prefix="/applies", tags=["applies"])
logger = logging.getLogger(__name__)


@router.post("/create_apply", response_model=schemas.Apply)
async def create_apply(
    apply: schemas.ApplyCreate, db: AsyncSession = Depends(get_async_db)
):
    """Создание нового отклика"""
    try:
        # Проверяем существование пользователя
        result = await db.execute(
            select(models.User).where(models.User.id == apply.user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        # Генерируем ID для отклика
        apply_id = models.Apply.generate_id(apply.user_id, apply.name)

        # Создаем отклик
        db_apply = models.Apply(
            id=apply_id,
            user_id=apply.user_id,
            name=apply.name,
            link=apply.link,
            description=apply.description,
        )
        db.add(db_apply)
        await db.commit()
        await db.refresh(db_apply)

        logger.info(f"Создан отклик {apply_id} для пользователя {apply.user_id}")
        return db_apply

    except Exception as e:
        logger.error(f"Ошибка создания отклика: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания отклика",
        )


@router.put("/update_apply/{apply_id}", response_model=schemas.Apply)
async def update_apply(
    apply_id: str,
    apply_update: schemas.ApplyUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """Обновление отклика"""
    try:
        result = await db.execute(
            select(models.Apply).where(models.Apply.id == apply_id)
        )
        db_apply = result.scalar_one_or_none()
        if not db_apply:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
            )

        # Обновляем поля
        update_data = apply_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apply, field, value)

        await db.commit()
        await db.refresh(db_apply)

        logger.info(f"Обновлен отклик {apply_id}")
        return db_apply

    except Exception as e:
        logger.error(f"Ошибка обновления отклика {apply_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления отклика",
        )


@router.delete("/delete_apply/{apply_id}")
async def delete_apply(apply_id: str, db: AsyncSession = Depends(get_async_db)):
    """Удаление отклика"""
    try:
        result = await db.execute(
            select(models.Apply).where(models.Apply.id == apply_id)
        )
        db_apply = result.scalar_one_or_none()
        if not db_apply:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
            )

        await db.delete(db_apply)
        await db.commit()

        logger.info(f"Удален отклик {apply_id}")
        return {"message": "Отклик удален"}

    except Exception as e:
        logger.error(f"Ошибка удаления отклика {apply_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления отклика",
        )


@router.get("/get_applies/{username}", response_model=List[schemas.Apply])
async def get_applies(username: str, db: AsyncSession = Depends(get_async_db)):
    """Получение всех откликов пользователя по username"""
    try:
        # Сначала находим пользователя по username
        result = await db.execute(
            select(models.User).where(models.User.username == username)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        # Получаем отклики пользователя
        result = await db.execute(
            select(models.Apply).where(models.Apply.user_id == user.id)
        )
        applies = result.scalars().all()
        logger.info(f"Получено {len(applies)} откликов для пользователя @{username}")
        return applies

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения откликов для пользователя @{username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения откликов",
        )
