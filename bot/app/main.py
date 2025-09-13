import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import app_config
from app.handlers import applies, commands, vacancy_handler

# Настройка логирования
logging.basicConfig(
    level=app_config.log_level,
    format=app_config.log_format,
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=app_config.telegram_bot_token)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(vacancy_handler.router)
dp.include_router(applies.router)


async def main():
    """Основная функция"""
    logger.info("Запуск Telegram бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
