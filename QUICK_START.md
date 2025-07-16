# Быстрый запуск Applyr

## 1. Подготовка

1. Скопируйте `env.example` в `.env`:
```bash
cp env.example .env
```

2. Отредактируйте `.env` и добавьте ваш Telegram Bot Token:
```env
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

## 2. Запуск

```bash
# Сборка и запуск всех сервисов
docker-compose up --build
```

## 3. Проверка

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 4. Использование бота

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Перешлите сообщение с вакансией
4. Используйте `/my_applies` для просмотра откликов

## 5. Остановка

```bash
docker-compose down
```

## Получение Telegram Bot Token

1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен в `.env`

## Новая структура бота

Бот теперь имеет модульную структуру:
- `handlers/` - обработчики сообщений и команд
- `services/` - бизнес-логика и API клиент
- `utils/` - утилиты для обработки текста 