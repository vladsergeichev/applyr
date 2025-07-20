import logging
from typing import List

from repositories.auth_repository import AuthRepository
from repositories.stage_repository import StageRepository
from repositories.vacancy_repository import VacancyRepository
from schemas.admin import StageResponse, TokenResponse, UserResponse, VacancyResponse

logger = logging.getLogger(__name__)


class AdminService:
    def __init__(
        self,
        auth_repo: AuthRepository,
        vacancy_repo: VacancyRepository,
        stage_repo: StageRepository,
    ):
        self.auth_repo = auth_repo
        self.vacancy_repo = vacancy_repo
        self.stage_repo = stage_repo

    async def get_all_users(self) -> List[UserResponse]:
        """Получает всех пользователей"""
        users = await self.auth_repo.get_all_users()
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                telegram_username=user.telegram_username,
                created_at=user.created_at,
            )
            for user in users
        ]

    async def get_all_vacancies(self) -> List[VacancyResponse]:
        """Получает все вакансии"""
        vacancies = await self.vacancy_repo.get_all()
        return [
            VacancyResponse(
                id=vacancy.id,
                name=vacancy.name,
                description=vacancy.description,
                link=vacancy.link,
                company_name=vacancy.company_name,
                user_id=vacancy.user_id,
                created_at=vacancy.created_at,
            )
            for vacancy in vacancies
        ]

    async def get_all_stages(self) -> List[StageResponse]:
        """Получает все этапы"""
        stages = await self.stage_repo.get_all()
        return [
            StageResponse(
                id=stage.id,
                name=stage.stage_type,
                description=stage.description,
                order_index=0,  # У StageModel нет order_index
                vacancy_id=stage.vacancy_id,
                created_at=stage.created_at,
            )
            for stage in stages
        ]

    async def get_all_tokens(self) -> List[TokenResponse]:
        """Получает все refresh токены"""
        tokens = await self.auth_repo.get_all_refresh_tokens()
        return [
            TokenResponse(
                id=token.id,
                token_hash=token.token_hash,
                user_id=token.user_id,
                expires_at=token.expires_at,
                created_at=token.created_at,
            )
            for token in tokens
        ]
