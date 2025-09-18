import logging

import aiohttp
from app.config import app_config

logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для работы с API"""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url or app_config.api_url

    async def create_vacancy(
        self, user_id: int, name: str, link: str, description: str
    ) -> tuple[bool, str]:
        """Создает отклик через API"""
        try:
            async with aiohttp.ClientSession() as session:
                apply_data = {
                    "user_id": user_id,
                    "name": name,
                    "link": link,
                    "description": description,
                }

                async with session.post(
                    f"{self.base_url}/api/internal/create_vacancy", json=apply_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Создан отклик: {result['id']}")
                        return True, result["id"]
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Ошибка создания отклика: {response.status} - {error_text}"
                        )
                        return False, f"Ошибка создания отклика: {response.status}"

        except Exception as e:
            logger.error(f"Ошибка при создании отклика: {e}")
            return False, f"Ошибка: {str(e)}"

    async def get_user_applies(self, username: str) -> list:
        """Получает вакансии пользователя по username"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/internal/get_vacancies/{username}"
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Ошибка получения откликов: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Ошибка получения откликов: {e}")
            return []

    async def get_user_by_telegram_username(self, telegram_username: str) -> int | None:
        """Возвращает user_id пользователя по telegram_username, если найден, иначе None"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/internal/get_by_telegram/{telegram_username}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("id")
                    return None
        except Exception as e:
            logger.error(f"Ошибка при проверке telegram_username: {e}")
            return None
