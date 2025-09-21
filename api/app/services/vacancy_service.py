import logging

from app.exceptions import UserNotFoundException, VacancyNotFoundException
from app.repositories.auth_repository import AuthRepository
from app.repositories.vacancy_repository import VacancyRepository
from app.schemas.vacancy import (
    GetVacancySchema,
    VacancyCreateSchema,
    VacancySchema,
    VacancyUpdateSchema,
)

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
            raise UserNotFoundException()

        vacancy = await self.vacancy_repo.create(vacancy_data)
        logger.info(
            f"Создана вакансия {vacancy.id} для пользователя {vacancy_data.user_id}"
        )
        return vacancy

    async def get_vacancy_by_id(self, vacancy_id: int) -> GetVacancySchema:
        """Получает вакансию по ID"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise VacancyNotFoundException()

        logger.info(f"Получена вакансия {vacancy_id}")
        return GetVacancySchema.model_validate(vacancy)

    async def get_vacancies_by_user_id(self, user_id: int) -> list[GetVacancySchema]:
        """Получает вакансии пользователя по username"""
        vacancies = await self.vacancy_repo.get_by_user_id(user_id)
        logger.info(f"Получено {len(vacancies)} вакансий для пользователя {user_id}")
        return vacancies

    async def update_vacancy(
        self, vacancy_id: int, vacancy_data: VacancyUpdateSchema
    ) -> VacancySchema:
        """Обновляет вакансию"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise VacancyNotFoundException()

        updated_vacancy = await self.vacancy_repo.update(vacancy_id, vacancy_data)
        logger.info(f"Обновлена вакансия {vacancy_id}")
        return updated_vacancy

    async def delete_vacancy(self, vacancy_id: int) -> None:
        """Удаляет вакансию"""
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise VacancyNotFoundException()

        await self.vacancy_repo.delete(vacancy_id)
        logger.info(f"Удалена вакансия {vacancy_id}")
