import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()


# @router.message(Command("start"))
# async def cmd_start(message: Message):
#     """Обработчик команды /start"""
#     await message.answer(
#         "Привет! Я бот для управления откликами на вакансии.\n\n"
#         "Перешлите мне сообщение с описанием вакансии, и я создам отклик."
#     )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """
🤖 <b>Как использовать бота:</b>

1. <b>Создание отклика:</b> Перешлите сообщение с описанием вакансии
2. <b>Просмотр откликов:</b> Используйте команду /my_applies
3. <b>Помощь:</b> /help

<b>Формат пересылаемого сообщения:</b>
- Первая строка будет использована как название вакансии
- Остальной текст сохранится как описание
    """
    await message.answer(help_text, parse_mode="HTML")
