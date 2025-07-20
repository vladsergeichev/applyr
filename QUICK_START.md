# 🚀 Быстрый старт Applyr

## 1. Подготовка

```bash
# Скопируйте и настройте переменные окружения
cp env.example .env
nano .env  # Добавьте ваш TELEGRAM_BOT_TOKEN
```

## 2. Запуск

### Для разработки (HTTP):
```bash
docker-compose up --build
```

### Для разработки с HTTPS:
```bash
docker-compose -f docker-compose.local.yml up -d --build
```

### Для продакшена:
```bash
./init-ssl.sh
docker-compose up -d
```

## 3. Проверка

- **API**: http://localhost:8000 (или https://localhost)
- **API Docs**: http://localhost:8000/docs (или https://localhost/docs)
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

## 📚 Дополнительная документация

- **[README.md](README.md)** - полная документация проекта
- **[DEPLOY.md](DEPLOY.md)** - инструкция по деплою на продакшен 