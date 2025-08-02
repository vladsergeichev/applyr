import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """
🤖 <b>Как использовать бота:</b>

1. <b>Сохранение вакансии:</b> Перешлите сообщение с описанием вакансии
2. <b>Просмотр вакансий:</b> Используйте команду /my_vacancies
3. <b>Помощь:</b> /help

<b>Формат пересылаемого сообщения:</b>
- Первая строка будет использована как название вакансии
- Остальной текст сохранится как описание
    """
    await message.answer(help_text, parse_mode="HTML")
