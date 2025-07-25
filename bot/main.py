import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import app_config
from handlers import applies, commands, vacancy_handler

# Настройка логирования
logging.basicConfig(
    level=app_config.LOG_LEVEL,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=app_config.TELEGRAM_BOT_TOKEN)
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
