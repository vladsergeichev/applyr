import logging
from typing import List, Optional

from core.exceptions import UserNotFoundError
from repositories.auth_repository import AuthRepository
from repositories.vacancy_repository import VacancyRepository
from schemas.vacancy import VacancyCreateSchema, VacancySchema, VacancyUpdateSchema

logger = logging.getLogger(__name__)


class VacancyService:
    def __init__(self, vacancy_repo: VacancyRepository, auth_repo: AuthRepository):
        self.vacancy_repo = vacancy_repo
        self.auth_repo = auth_repo

    async def create_vacancy(self, vacancy_data: VacancyCreateSchema) -> VacancySchema:
        """Создает новую вакансию"""
        # Проверяем, существует ли пользователь
        user = await self.auth_repo.get_by_id(vacancy_data.user_id)
        if not user:
            raise UserNotFoundError(
                f"Пользователь с ID {vacancy_data.user_id} не найден"
            )

        vacancy = await self.vacancy_repo.create(vacancy_data)
        logger.info(
            f"Создана вакансия {vacancy.id} для пользователя {vacancy_data.user_id}"
        )
        return vacancy

    async def get_vacancy_by_id(self, vacancy_id: int) -> Optional[VacancySchema]:
        """Получает вакансию по ID"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            return None

        logger.info(f"Получена вакансия {vacancy_id}")
        return vacancy

    async def get_vacancies_by_username(self, username: str) -> List[VacancySchema]:
        """Получает вакансии пользователя по username"""
        user = await self.auth_repo.get_by_username(username)
        if not user:
            logger.warning(f"Пользователь с username '{username}' не найден")
            return []

        vacancies = await self.vacancy_repo.get_by_user_id(user.id)
        logger.info(f"Получено {len(vacancies)} вакансий для пользователя @{username}")
        return vacancies

    async def update_vacancy(
        self, vacancy_id: int, vacancy_data: VacancyUpdateSchema
    ) -> Optional[VacancySchema]:
        """Обновляет вакансию"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            return None

        updated_vacancy = await self.vacancy_repo.update(vacancy_id, vacancy_data)
        logger.info(f"Обновлена вакансия {vacancy_id}")
        return updated_vacancy

    async def delete_vacancy(self, vacancy_id: int) -> bool:
        """Удаляет вакансию"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            return False

        await self.vacancy_repo.delete(vacancy_id)
        logger.info(f"Удалена вакансия {vacancy_id}")
        return True
