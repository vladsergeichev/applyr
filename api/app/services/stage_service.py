import logging

from app.exceptions import StageNotFoundException, VacancyNotFoundException
from app.repositories.stage_repository import StageRepository
from app.repositories.vacancy_repository import VacancyRepository
from app.schemas.stage import StageCreateSchema, StageSchema, StageUpdateSchema

logger = logging.getLogger(__name__)


class StageService:
    def __init__(self, stage_repo: StageRepository, vacancy_repo: VacancyRepository):
        self.stage_repo = stage_repo
        self.vacancy_repo = vacancy_repo

    async def create_stage(self, stage_data: StageCreateSchema) -> StageSchema:
        """Создает новый этап"""
        # Проверяем, существует ли вакансия
        vacancy = await self.vacancy_repo.get_by_id(stage_data.vacancy_id)
        if not vacancy:
            raise VacancyNotFoundException()

        stage = await self.stage_repo.create(stage_data)
        logger.info(f"Создан этап {stage.id} для вакансии {stage_data.vacancy_id}")
        return stage

    async def get_stage_by_id(self, stage_id: int) -> StageSchema:
        """Получает этап по ID"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            raise StageNotFoundException()

        logger.info(f"Получен этап {stage_id}")
        return stage

    async def get_stages_by_vacancy_id(self, vacancy_id: int) -> list[StageSchema]:
        """Получает этапы вакансии"""
        # Проверяем, существует ли вакансия
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            raise VacancyNotFoundException()

        stages = await self.stage_repo.get_by_vacancy_id(vacancy_id)
        logger.info(f"Получено {len(stages)} этапов для вакансии {vacancy_id}")
        return stages

    async def update_stage(
        self, stage_id: int, stage_data: StageUpdateSchema
    ) -> StageSchema:
        """Обновляет этап"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            raise StageNotFoundException()

        updated_stage = await self.stage_repo.update(stage_id, stage_data)
        logger.info(f"Обновлен этап {stage_id}")
        return updated_stage

    async def delete_stage(self, stage_id: int) -> None:
        """Удаляет этап"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            raise StageNotFoundException()

        await self.stage_repo.delete(stage_id)
        logger.info(f"Удален этап {stage_id}")
