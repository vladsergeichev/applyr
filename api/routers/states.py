import logging

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_db

router = APIRouter(prefix="/states", tags=["states"])
logger = logging.getLogger(__name__)


@router.post("/create_state", response_model=schemas.State)
async def create_state(
    state: schemas.StateCreate, db: AsyncSession = Depends(get_async_db)
):
    """Создание нового состояния"""
    try:
        # Проверяем уникальность имени
        result = await db.execute(
            select(models.State).where(models.State.name == state.name)
        )
        existing_state = result.scalar_one_or_none()
        if existing_state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Состояние с таким именем уже существует",
            )

        # Создаем состояние
        db_state = models.State(name=state.name)
        db.add(db_state)
        await db.commit()
        await db.refresh(db_state)

        logger.info(f"Создано состояние '{state.name}' с ID {db_state.id}")
        return db_state

    except Exception as e:
        logger.error(f"Ошибка создания состояния: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания состояния",
        )


@router.put("/update_state/{state_id}", response_model=schemas.State)
async def update_state(
    state_id: int,
    state_update: schemas.StateUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """Обновление состояния"""
    try:
        result = await db.execute(
            select(models.State).where(models.State.id == state_id)
        )
        db_state = result.scalar_one_or_none()
        if not db_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Состояние не найдено"
            )

        # Проверяем уникальность нового имени
        if state_update.name != db_state.name:
            result = await db.execute(
                select(models.State).where(models.State.name == state_update.name)
            )
            existing_state = result.scalar_one_or_none()
            if existing_state:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Состояние с таким именем уже существует",
                )

        # Обновляем имя
        db_state.name = state_update.name
        await db.commit()
        await db.refresh(db_state)

        logger.info(f"Обновлено состояние {state_id}: '{db_state.name}'")
        return db_state

    except Exception as e:
        logger.error(f"Ошибка обновления состояния {state_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления состояния",
        )


@router.delete("/delete_state/{state_id}")
async def delete_state(state_id: int, db: AsyncSession = Depends(get_async_db)):
    """Удаление состояния"""
    try:
        result = await db.execute(
            select(models.State).where(models.State.id == state_id)
        )
        db_state = result.scalar_one_or_none()
        if not db_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Состояние не найдено"
            )

        # Проверяем, используется ли состояние
        result = await db.execute(
            select(models.ApplyState).where(models.ApplyState.state_id == state_id)
        )
        apply_states = result.scalar_one_or_none()
        if apply_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нельзя удалить состояние, которое используется в откликах",
            )

        await db.delete(db_state)
        await db.commit()

        logger.info(f"Удалено состояние {state_id}")
        return {"message": "Состояние удалено"}

    except Exception as e:
        logger.error(f"Ошибка удаления состояния {state_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления состояния",
        )


@router.post("/create_apply_state", response_model=schemas.ApplyState)
async def create_apply_state(
    apply_state: schemas.ApplyStateCreate, db: AsyncSession = Depends(get_async_db)
):
    """Создание нового состояния отклика"""
    try:
        # Проверяем существование отклика
        result = await db.execute(
            select(models.Apply).where(models.Apply.id == apply_state.apply_id)
        )
        apply = result.scalar_one_or_none()
        if not apply:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
            )

        # Проверяем существование состояния
        result = await db.execute(
            select(models.State).where(models.State.id == apply_state.state_id)
        )
        state = result.scalar_one_or_none()
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Состояние не найдено"
            )

        # Генерируем ID для состояния отклика
        apply_state_id = models.ApplyState.generate_id(
            apply_state.apply_id, apply_state.state_id
        )

        # Создаем состояние отклика
        db_apply_state = models.ApplyState(
            id=apply_state_id,
            apply_id=apply_state.apply_id,
            state_id=apply_state.state_id,
            description=apply_state.description,
            occurred_at=apply_state.occurred_at,
        )
        db.add(db_apply_state)
        await db.commit()
        await db.refresh(db_apply_state)

        logger.info(
            f"Создано состояние отклика {apply_state_id} для отклика {apply_state.apply_id}"
        )
        return db_apply_state

    except Exception as e:
        logger.error(f"Ошибка создания состояния отклика: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания состояния отклика",
        )


@router.put("/update_apply_state/{apply_state_id}", response_model=schemas.ApplyState)
async def update_apply_state(
    apply_state_id: str,
    apply_state_update: schemas.ApplyStateUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """Обновление состояния отклика"""
    try:
        result = await db.execute(
            select(models.ApplyState).where(models.ApplyState.id == apply_state_id)
        )
        db_apply_state = result.scalar_one_or_none()
        if not db_apply_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Состояние отклика не найдено",
            )

        # Обновляем поля
        update_data = apply_state_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apply_state, field, value)

        await db.commit()
        await db.refresh(db_apply_state)

        logger.info(f"Обновлено состояние отклика {apply_state_id}")
        return db_apply_state

    except Exception as e:
        logger.error(f"Ошибка обновления состояния отклика {apply_state_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления состояния отклика",
        )


@router.delete("/delete_apply_state/{apply_state_id}")
async def delete_apply_state(
    apply_state_id: str, db: AsyncSession = Depends(get_async_db)
):
    """Удаление состояния отклика"""
    try:
        result = await db.execute(
            select(models.ApplyState).where(models.ApplyState.id == apply_state_id)
        )
        db_apply_state = result.scalar_one_or_none()
        if not db_apply_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Состояние отклика не найдено",
            )

        await db.delete(db_apply_state)
        await db.commit()

        logger.info(f"Удалено состояние отклика {apply_state_id}")
        return {"message": "Состояние отклика удалено"}

    except Exception as e:
        logger.error(f"Ошибка удаления состояния отклика {apply_state_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления состояния отклика",
        )
