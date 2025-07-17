import logging
from typing import List

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/applies", tags=["applies"])
logger = logging.getLogger(__name__)


@router.post("/create_apply", response_model=schemas.Apply)
def create_apply(apply: schemas.ApplyCreate, db: Session = Depends(get_db)):
    """Создание нового отклика"""
    try:
        # Проверяем существование пользователя
        user = db.query(models.User).filter(models.User.id == apply.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

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
        db.commit()
        db.refresh(db_apply)

        logger.info(f"Создан отклик {apply_id} для пользователя {apply.user_id}")
        return db_apply

    except Exception as e:
        logger.error(f"Ошибка создания отклика: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка создания отклика")


@router.put("/update_apply/{apply_id}", response_model=schemas.Apply)
def update_apply(
    apply_id: str, apply_update: schemas.ApplyUpdate, db: Session = Depends(get_db)
):
    """Обновление отклика"""
    try:
        db_apply = db.query(models.Apply).filter(models.Apply.id == apply_id).first()
        if not db_apply:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        # Обновляем поля
        update_data = apply_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apply, field, value)

        db.commit()
        db.refresh(db_apply)

        logger.info(f"Обновлен отклик {apply_id}")
        return db_apply

    except Exception as e:
        logger.error(f"Ошибка обновления отклика {apply_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка обновления отклика")


@router.delete("/delete_apply/{apply_id}")
def delete_apply(apply_id: str, db: Session = Depends(get_db)):
    """Удаление отклика"""
    try:
        db_apply = db.query(models.Apply).filter(models.Apply.id == apply_id).first()
        if not db_apply:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        db.delete(db_apply)
        db.commit()

        logger.info(f"Удален отклик {apply_id}")
        return {"message": "Отклик удален"}

    except Exception as e:
        logger.error(f"Ошибка удаления отклика {apply_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка удаления отклика")


@router.get("/get_applies/{username}", response_model=List[schemas.Apply])
def get_applies(username: str, db: Session = Depends(get_db)):
    """Получение всех откликов пользователя по username"""
    try:
        # Сначала находим пользователя по username
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем отклики пользователя
        applies = db.query(models.Apply).filter(models.Apply.user_id == user.id).all()
        logger.info(f"Получено {len(applies)} откликов для пользователя @{username}")
        return applies

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения откликов для пользователя @{username}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения откликов")
