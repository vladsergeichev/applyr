import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.api_client import APIClient

logger = logging.getLogger(__name__)
router = Router()
api_client = APIClient()


@router.message(Command("my_applies"))
async def cmd_my_applies(message: Message):
    """Показывает все отклики пользователя"""
    try:
        applies = await api_client.get_user_applies(message.from_user.id)

        if applies:
            text = "📋 <b>Ваши отклики:</b>\n\n"
            for i, apply in enumerate(applies[:10], 1):  # Показываем первые 10
                text += f"{i}. <b>{apply['name']}</b>\n"
                text += f"   📅 {apply['created_at'][:10]}\n"
                text += f"   🔗 <a href=\"{apply['link']}\">Ссылка</a>\n\n"

            if len(applies) > 10:
                text += f"... и еще {len(applies) - 10} откликов"
        else:
            text = "У вас пока нет откликов. Перешлите сообщение с вакансией!"

        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"Ошибка получения откликов: {e}")
        await message.answer("Ошибка получения откликов")
