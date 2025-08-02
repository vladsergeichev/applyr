from fastapi import APIRouter, Depends
from routers.public import auth, stage, vacancy
from routers.admin import admin
from routers.internal import bot

admin_router = APIRouter(
    prefix="/admin",
    # dependencies=[Depends(admin_authenticate)],
)
admin_router.include_router(
    admin.router,
    tags=["Админка для разработки"],
)


internal_router = APIRouter(
    prefix="/internal",
    # dependencies=[Depends(internal_authenticate)],
)
internal_router.include_router(
    bot.router,
    tags=["Взаимодействие с ботом"],
)


public_router = APIRouter(
    prefix="/public",
    # dependencies=[Depends(authenticate)],
)
public_router.include_router(
    auth.router,
    tags=["Аутентификация"],
)
public_router.include_router(
    vacancy.router,
    tags=["Вакансии"],
)
public_router.include_router(
    stage.router,
    tags=["Этапы"],
)
