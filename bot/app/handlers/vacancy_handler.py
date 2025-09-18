import logging

from aiogram import Router
from aiogram.types import Message

from app.services.api_client import APIClient
from app.utils.text_processor import extract_vacancy_name, generate_link

logger = logging.getLogger(__name__)
router = Router()
api_client = APIClient()


@router.message()
async def handle_message(message: Message):
    """Обработчик всех сообщений"""
    # Проверяем, знаем ли пользователя
    username = message.from_user.username
    user_id = await api_client.get_user_by_telegram_username(username)
    if not user_id:
        await message.answer(
            "Вы не зарегистрированы в системе. Пожалуйста, перейдите на сайт https://applyr.vladsergeichev.ru и зарегистрируйтесь. После этого вы сможете пользоваться ботом."
        )
        return

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
    description = message.text

    # Создаем
    success, result = await api_client.create_vacancy(
        user_id, vacancy_name, link, description
    )

    if success:
        await message.answer(
            f"✅ <b>Вакансия сохранена!</b>\n\n"
            f"<b>Вакансия:</b> {vacancy_name}\n"
            f'<b>Ссылка:</b> <a href="{link}">Перейти к посту</a>\n\n'
            f"Используйте /my_vacancies для просмотра всех вакансий\n"
            f"Или заходите на сайт applyr.vladsergeichev.ru",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        await message.answer(f"❌ {result}")
