import logging

from core.dependencies import get_user_service
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreateSchema, UserSchema
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.post("/create_user", response_model=UserSchema)
async def create_user(
    user: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    """Создание нового пользователя"""
    try:
        return await user_service.create_user(user.id, user.name, user.username)
    except Exception as e:
        logger.error(f"Ошибка создания пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания пользователя",
        )
