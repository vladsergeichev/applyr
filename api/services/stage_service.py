import logging
from typing import List, Optional

from core.exceptions import VacancyNotFoundError
from repositories.stage_repository import StageRepository
from repositories.vacancy_repository import VacancyRepository
from schemas.stage import StageCreateSchema, StageSchema, StageUpdateSchema

logger = logging.getLogger(__name__)


class StageService:
    def __init__(self, stage_repo: StageRepository, vacancy_repo: VacancyRepository):
        self.stage_repo = stage_repo
        self.vacancy_repo = vacancy_repo

    async def create_stage(self, stage_data: StageCreateSchema) -> StageSchema:
        """Создает новый этап"""
        # Проверяем, существует ли вакансия
        vacancy = await self.vacancy_repo.get_by_id(stage_data.apply_id)
        if not vacancy:
            raise VacancyNotFoundError(
                f"Вакансия с ID {stage_data.apply_id} не найдена"
            )

        stage = await self.stage_repo.create(stage_data)
        logger.info(f"Создан этап {stage.id} для вакансии {stage_data.apply_id}")
        return stage

    async def get_stage_by_id(self, stage_id: int) -> Optional[StageSchema]:
        """Получает этап по ID"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            return None

        logger.info(f"Получен этап {stage_id}")
        return stage

    async def get_stages_by_vacancy_id(self, vacancy_id: int) -> List[StageSchema]:
        """Получает все этапы вакансии"""
        # Проверяем, существует ли вакансия
        vacancy = await self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy:
            logger.warning(f"Вакансия с ID {vacancy_id} не найдена")
            return []

        stages = await self.stage_repo.get_by_vacancy_id(vacancy_id)
        logger.info(f"Получено {len(stages)} этапов для вакансии {vacancy_id}")
        return stages

    async def update_stage(
        self, stage_id: int, stage_data: StageUpdateSchema
    ) -> Optional[StageSchema]:
        """Обновляет этап"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            return None

        updated_stage = await self.stage_repo.update(stage_id, stage_data)
        logger.info(f"Обновлен этап {stage_id}")
        return updated_stage

    async def delete_stage(self, stage_id: int) -> bool:
        """Удаляет этап"""
        stage = await self.stage_repo.get_by_id(stage_id)
        if not stage:
            return False

        await self.stage_repo.delete(stage_id)
        logger.info(f"Удален этап {stage_id}")
        return True
