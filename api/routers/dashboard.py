import models
from config import templates
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = None):
    """Дашборд для просмотра откликов пользователя по username"""
    applies = None
    error_message = None
    if username:
        try:
            db = next(get_db())
            user = (
                db.query(models.User).filter(models.User.username == username).first()
            )
            if not user:
                error_message = f"Пользователь с username @{username} не найден"
            else:
                applies = (
                    db.query(models.Apply)
                    .filter(models.Apply.user_id == user.id)
                    .order_by(models.Apply.created_at.desc())
                    .all()
                )
        except Exception as e:
            error_message = f"Ошибка при получении данных: {str(e)}"
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "username": username,
            "applies": applies,
            "error_message": error_message,
        },
    )


@router.delete("/dashboard/delete/{apply_id}")
async def delete_apply(apply_id: str):
    """Удаляет отклик по ID"""
    try:
        db = next(get_db())
        apply = db.query(models.Apply).filter(models.Apply.id == apply_id).first()

        if not apply:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        db.delete(apply)
        db.commit()

        return {"message": "Отклик успешно удален"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {str(e)}")
