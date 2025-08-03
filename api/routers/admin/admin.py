from typing import List

from core.dependencies import get_admin_service
from fastapi import APIRouter, Depends
from schemas.admin import StageResponse, TokenResponse, UserResponse, VacancyResponse
from services.admin_service import AdminService

router = APIRouter()


@router.get("/get_users", response_model=List[UserResponse])
async def get_users(admin_service: AdminService = Depends(get_admin_service)):
    """Получить всех пользователей"""
    return await admin_service.get_all_users()


@router.get("/get_vacancies", response_model=List[VacancyResponse])
async def get_vacancies(admin_service: AdminService = Depends(get_admin_service)):
    """Получить все вакансии"""
    return await admin_service.get_all_vacancies()


@router.get("/get_stages")
async def get_stages(admin_service: AdminService = Depends(get_admin_service)):
    """Получить все этапы"""
    return await admin_service.get_all_stages()


@router.get("/get_tokens", response_model=List[TokenResponse])
async def get_tokens(admin_service: AdminService = Depends(get_admin_service)):
    """Получить все refresh токены"""
    return await admin_service.get_all_tokens()
