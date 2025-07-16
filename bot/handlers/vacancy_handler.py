import logging

from aiogram import Router
from aiogram.types import Message
from services.api_client import APIClient
from utils.text_processor import extract_vacancy_name, generate_link

logger = logging.getLogger(__name__)
router = Router()
api_client = APIClient()


@router.message()
async def handle_message(message: Message):
    """Обработчик всех сообщений"""
    # Проверяем, что это пересланное сообщение
    if not message.forward_from_chat:
        await message.answer(
            "Пожалуйста, перешлите сообщение с описанием вакансии.\n"
            "Используйте /help для получения справки."
        )
        return

    # Извлекаем название вакансии из текста
    if not message.text:
        await message.answer("Сообщение должно содержать текст с описанием вакансии.")
        return

    vacancy_name = extract_vacancy_name(message.text)
    link = generate_link(message.forward_from_chat.id, message.forward_from_message_id)

    # Создаем пользователя, если его нет
    await api_client.create_user(
        message.from_user.id, message.from_user.username, message.from_user.first_name
    )

    # Создаем отклик
    success, result = await api_client.create_apply(
        message.from_user.id, vacancy_name, link
    )

    if success:
        await message.answer(
            f"✅ <b>Отклик создан!</b>\n\n"
            f"<b>Вакансия:</b> {vacancy_name}\n"
            f"<b>Ссылка:</b> <a href=\"{link}\">Перейти к посту</a>\n\n"
            f"Используйте /my_applies для просмотра всех откликов",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        await message.answer(f"❌ {result}")
