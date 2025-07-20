# Applyr - Система управления откликами на вакансии

Система для автоматического создания и управления откликами на вакансии через Telegram бот.

## Архитектура

Проект состоит из трех основных компонентов:

1. **Telegram Bot** (aiogram) - получает пересланные сообщения с вакансиями
2. **FastAPI Server** - REST API для управления откликами и состояниями
3. **PostgreSQL Database** - хранение данных пользователей, откликов и состояний

## Структура проекта

```
applyr/
├── docker-compose.yml          # Оркестрация контейнеров
├── database/
│   └── init.sql               # Инициализация БД
├── api/                       # FastAPI сервер
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py               # Основное приложение
│   ├── database.py           # Настройка БД
│   ├── models.py             # SQLAlchemy модели
│   ├── schemas.py            # Pydantic схемы
│   └── routers/              # API роутеры
│       ├── applies.py        # Управление откликами
│       ├── states.py         # Управление состояниями
│       └── users.py          # Управление пользователями
└── bot/                     # Telegram бот
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py             # Основной файл бота
    ├── config.py           # Конфигурация
    ├── handlers/           # Обработчики сообщений
    │   ├── commands.py     # Команды бота
    │   ├── applies.py      # Работа с откликами
    │   └── vacancy_handler.py # Обработка вакансий
    ├── services/           # Сервисы
    │   └── api_client.py   # Клиент для API
    └── utils/              # Утилиты
        └── text_processor.py # Обработка текста
```

## База данных

### Таблицы:
- **users** - пользователи (telegram_id, username, name, created_at)
- **applies** - отклики (id, user_id, name, link, description, timestamps)
- **states** - состояния (id, name)
- **apply_states** - состояния откликов (id, vacancy_id, state_id, description, timestamps)

### Базовые состояния:
- Создан
- Отправлено
- Ответ получен
- Приглашение на собеседование
- Собеседование пройдено
- Отклонено
- Принят

## API Endpoints

### Отклики (/applies)
- `POST /create_apply` - создание отклика
- `PUT /update_apply/{id}` - обновление отклика
- `DELETE /delete_apply/{id}` - удаление отклика
- `GET /get_applies/{username}` - получение откликов пользователя по username

### Состояния (/states)
- `POST /create_state` - создание состояния
- `PUT /update_state/{id}` - обновление состояния
- `DELETE /delete_state/{id}` - удаление состояния
- `POST /create_apply_state` - создание состояния отклика
- `PUT /update_apply_state/{id}` - обновление состояния отклика
- `DELETE /delete_apply_state/{id}` - удаление состояния отклика

### Пользователи (/users)
- `POST /create_user` - создание пользователя

## Telegram Bot

### Команды:
- `/start` - приветствие и инструкции
- `/help` - справка по использованию
- `/my_applies` - просмотр всех откликов пользователя

### Функциональность:
- Обработка пересланных сообщений с вакансиями
- Автоматическое извлечение названия вакансии из первой строки
- Создание ссылки на оригинальный пост
- Интеграция с API для сохранения данных

## Запуск проекта

### 1. Подготовка

Создайте файл `.env` в корне проекта:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 2. Запуск через Docker Compose

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build
```

### 3. Проверка работы

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

### 4. Остановка

```bash
docker-compose down
```

## Разработка

### Локальная разработка

1. Установите зависимости:
```bash
# API
cd api
pip install -r requirements.txt

# Telegram Bot
cd ../bot
pip install -r requirements.txt
```

2. Запустите PostgreSQL:
```bash
docker run -d --name postgres \
  -e POSTGRES_DB=applyr \
  -e POSTGRES_USER=applyr_user \
  -e POSTGRES_PASSWORD=applyr_password \
  -p 5432:5432 \
  postgres:15
```

3. Запустите API:
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Запустите бота:
```bash
cd bot
python main.py
```

## Технологии

- **Python 3.12.10**
- **FastAPI** - веб-фреймворк для API
- **SQLAlchemy** - ORM для работы с БД
- **aiogram** - библиотека для Telegram ботов
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация контейнеров 