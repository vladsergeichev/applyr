import models
from config import templates
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from starlette import status

from database import get_async_db

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = None):
    """Дашборд для просмотра откликов пользователя по username"""
    applies = None
    error_message = None
    if username:
        try:
            async for db in get_async_db():
                # Сначала находим пользователя по username
                result = await db.execute(
                    select(models.User).where(models.User.username == username)
                )
                user = result.scalar_one_or_none()
                if not user:
                    error_message = f"Пользователь с username @{username} не найден"
                else:
                    # Получаем отклики пользователя
                    result = await db.execute(
                        select(models.Apply)
                        .where(models.Apply.user_id == user.id)
                        .order_by(models.Apply.created_at.desc())
                    )
                    applies = result.scalars().all()
                break
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
        async for db in get_async_db():
            result = await db.execute(
                select(models.Apply).where(models.Apply.id == apply_id)
            )
            apply = result.scalar_one_or_none()

            if not apply:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
                )

            await db.delete(apply)
            await db.commit()
            break

        return {"message": "Отклик успешно удален"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении: {str(e)}",
        )
