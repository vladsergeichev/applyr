import logging

import models
import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    try:
        # Проверяем, существует ли пользователь
        existing_user = db.query(models.User).filter(models.User.id == user.id).first()
        if existing_user:
            return existing_user  # Возвращаем существующего пользователя

        # Создаем нового пользователя
        db_user = models.User(id=user.id, name=user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"Создан пользователь {user.id}: {user.name}")
        return db_user

    except Exception as e:
        logger.error(f"Ошибка создания пользователя: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка создания пользователя")
