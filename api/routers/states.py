import logging
from typing import List

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/states", tags=["states"])
logger = logging.getLogger(__name__)


@router.post("/create_state", response_model=schemas.State)
def create_state(state: schemas.StateCreate, db: Session = Depends(get_db)):
    """Создание нового состояния"""
    try:
        # Проверяем уникальность имени
        existing_state = (
            db.query(models.State).filter(models.State.name == state.name).first()
        )
        if existing_state:
            raise HTTPException(
                status_code=400, detail="Состояние с таким именем уже существует"
            )

        # Создаем состояние
        db_state = models.State(name=state.name)
        db.add(db_state)
        db.commit()
        db.refresh(db_state)

        logger.info(f"Создано состояние '{state.name}' с ID {db_state.id}")
        return db_state

    except Exception as e:
        logger.error(f"Ошибка создания состояния: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка создания состояния")


@router.put("/update_state/{state_id}", response_model=schemas.State)
def update_state(
    state_id: int, state_update: schemas.StateUpdate, db: Session = Depends(get_db)
):
    """Обновление состояния"""
    try:
        db_state = db.query(models.State).filter(models.State.id == state_id).first()
        if not db_state:
            raise HTTPException(status_code=404, detail="Состояние не найдено")

        # Проверяем уникальность нового имени
        if state_update.name != db_state.name:
            existing_state = (
                db.query(models.State)
                .filter(models.State.name == state_update.name)
                .first()
            )
            if existing_state:
                raise HTTPException(
                    status_code=400, detail="Состояние с таким именем уже существует"
                )

        # Обновляем имя
        db_state.name = state_update.name
        db.commit()
        db.refresh(db_state)

        logger.info(f"Обновлено состояние {state_id}: '{db_state.name}'")
        return db_state

    except Exception as e:
        logger.error(f"Ошибка обновления состояния {state_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка обновления состояния")


@router.delete("/delete_state/{state_id}")
def delete_state(state_id: int, db: Session = Depends(get_db)):
    """Удаление состояния"""
    try:
        db_state = db.query(models.State).filter(models.State.id == state_id).first()
        if not db_state:
            raise HTTPException(status_code=404, detail="Состояние не найдено")

        # Проверяем, используется ли состояние
        apply_states = (
            db.query(models.ApplyState)
            .filter(models.ApplyState.state_id == state_id)
            .first()
        )
        if apply_states:
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить состояние, которое используется в откликах",
            )

        db.delete(db_state)
        db.commit()

        logger.info(f"Удалено состояние {state_id}")
        return {"message": "Состояние удалено"}

    except Exception as e:
        logger.error(f"Ошибка удаления состояния {state_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка удаления состояния")


@router.post("/create_apply_state", response_model=schemas.ApplyState)
def create_apply_state(
    apply_state: schemas.ApplyStateCreate, db: Session = Depends(get_db)
):
    """Создание нового состояния отклика"""
    try:
        # Проверяем существование отклика
        apply = (
            db.query(models.Apply)
            .filter(models.Apply.id == apply_state.apply_id)
            .first()
        )
        if not apply:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        # Проверяем существование состояния
        state = (
            db.query(models.State)
            .filter(models.State.id == apply_state.state_id)
            .first()
        )
        if not state:
            raise HTTPException(status_code=404, detail="Состояние не найдено")

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
        db.commit()
        db.refresh(db_apply_state)

        logger.info(
            f"Создано состояние отклика {apply_state_id} для отклика {apply_state.apply_id}"
        )
        return db_apply_state

    except Exception as e:
        logger.error(f"Ошибка создания состояния отклика: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка создания состояния отклика")


@router.put("/update_apply_state/{apply_state_id}", response_model=schemas.ApplyState)
def update_apply_state(
    apply_state_id: str,
    apply_state_update: schemas.ApplyStateUpdate,
    db: Session = Depends(get_db),
):
    """Обновление состояния отклика"""
    try:
        db_apply_state = (
            db.query(models.ApplyState)
            .filter(models.ApplyState.id == apply_state_id)
            .first()
        )
        if not db_apply_state:
            raise HTTPException(status_code=404, detail="Состояние отклика не найдено")

        # Обновляем поля
        update_data = apply_state_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apply_state, field, value)

        db.commit()
        db.refresh(db_apply_state)

        logger.info(f"Обновлено состояние отклика {apply_state_id}")
        return db_apply_state

    except Exception as e:
        logger.error(f"Ошибка обновления состояния отклика {apply_state_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Ошибка обновления состояния отклика"
        )


@router.delete("/delete_apply_state/{apply_state_id}")
def delete_apply_state(apply_state_id: str, db: Session = Depends(get_db)):
    """Удаление состояния отклика"""
    try:
        db_apply_state = (
            db.query(models.ApplyState)
            .filter(models.ApplyState.id == apply_state_id)
            .first()
        )
        if not db_apply_state:
            raise HTTPException(status_code=404, detail="Состояние отклика не найдено")

        db.delete(db_apply_state)
        db.commit()

        logger.info(f"Удалено состояние отклика {apply_state_id}")
        return {"message": "Состояние отклика удалено"}

    except Exception as e:
        logger.error(f"Ошибка удаления состояния отклика {apply_state_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка удаления состояния отклика")
