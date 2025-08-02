import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.api_client import APIClient

logger = logging.getLogger(__name__)
router = Router()
api_client = APIClient()


@router.message(Command("my_vacancies"))
async def cmd_my_vacancies(message: Message):
    """Показывает все вакансии пользователя"""
    # Проверяем, знаем ли пользователя
    username = message.from_user.username
    if not username or not await api_client.get_user_by_telegram_username(username):
        await message.answer(
            "Вы не зарегистрированы в системе. Пожалуйста, перейдите на сайт https://applyr.vladsergeichev.ru и зарегистрируйтесь, используя ваш Telegram username. После этого вы сможете пользоваться ботом."
        )
        return
    try:
        # Используем username пользователя, если он есть, иначе используем user_id как строку
        applies = await api_client.get_user_applies(username)

        if applies:
            text = "📋 <b>Ваши вакансии:</b>\n\n"
            for i, apply in enumerate(applies[:10], 1):  # Показываем первые 10
                text += f"{i}. <b>{apply['name']}</b>\n"
                text += f"   📅 {apply['created_at'][:10]}\n"
                text += f"   🔗 <a href=\"{apply['link']}\">Ссылка</a>\n\n"

            if len(applies) > 10:
                text += f"... и еще {len(applies) - 10} вакансий"
        else:
            text = "У вас пока нет сохраненных вакансий. Перешлите сообщение с вакансией!"

        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"Ошибка получения вакансий: {e}")
        await message.answer(
            "Произошла ошибка при получении вакансий. Попробуйте позже."
        )
