import logging

import aiohttp
from config import app_config

logger = logging.getLogger(__name__)


class APIClient:
    """Клиент для работы с API"""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url or app_config.API_URL

    async def create_user(self, user_id: int, username: str, first_name: str) -> bool:
        """Создает пользователя в базе данных, если его нет"""
        try:
            async with aiohttp.ClientSession() as session:
                user_data = {
                    "id": user_id,
                    "name": f"{first_name} ({username})" if username else first_name,
                    "username": username,
                }

                # Пытаемся создать пользователя (может уже существовать)
                async with session.post(
                    f"{self.base_url}/users/create_user", json=user_data
                ) as response:
                    if response.status not in [200, 409]:  # 409 - уже существует
                        logger.error(f"Ошибка создания пользователя: {response.status}")
                        return False
                    return True

        except Exception as e:
            logger.error(f"Ошибка при создании пользователя: {e}")
            return False

    async def create_apply(
        self, user_id: int, name: str, link: str
    ) -> tuple[bool, str]:
        """Создает отклик через API"""
        try:
            async with aiohttp.ClientSession() as session:
                apply_data = {
                    "user_id": user_id,
                    "name": name,
                    "link": link,
                    "description": "Создано через Telegram бот",
                }

                async with session.post(
                    f"{self.base_url}/applies/create_apply", json=apply_data
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
        """Получает отклики пользователя по username"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/applies/get_applies/{username}"
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Ошибка получения откликов: {response.status}")
                        return []

        except Exception as e:
            logger.error(f"Ошибка получения откликов: {e}")
            return []
