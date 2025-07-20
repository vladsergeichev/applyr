# 🚀 Деплой Applyr с SSL сертификатами

## Подготовка к деплою

### 1. Требования к серверу
- Ubuntu 20.04+ или аналогичный Linux
- Docker и Docker Compose
- Домен (например, `applyr.yourdomain.com`)
- Email для Let's Encrypt

### 2. Настройка переменных окружения

Создайте файл `.env`:
```env
# Логирование
LOG_LEVEL=INFO

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here

# База данных
DB_USER=applyr_user
DB_PASS=secure_password_here
DB_NAME=applyr_db
DB_HOST=postgres
DB_PORT=5432

# JWT Secret Key (сгенерируйте безопасный ключ)
SECRET_KEY=your_very_secure_secret_key_here

# HTTPS настройки
USE_HTTPS=true
DOMAIN=applyr.yourdomain.com
EMAIL=your_email@domain.com

# API URL для бота
API_URL=https://yourdomain.com
```

### 3. Настройка DNS

Настройте DNS записи для вашего домена:
```
A    applyr.yourdomain.com    →    IP_ВАШЕГО_СЕРВЕРА
```

## Деплой приложения

### 1. Клонирование и настройка
```bash
# Клонируйте репозиторий на сервер
git clone <your-repo-url>
cd applyr

# Создайте .env файл
cp env.example .env
nano .env  # Отредактируйте переменные
```

### 2. Первоначальное получение SSL сертификатов
```bash
# Запустите скрипт для получения сертификатов
./init-ssl.sh
```

### 3. Запуск всех сервисов
```bash
# Запустите все сервисы
docker-compose up -d

# Проверьте статус
docker-compose ps
```

### 4. Проверка работоспособности
```bash
# Проверьте логи
docker-compose logs -f

# Проверьте API
curl https://yourdomain.com/health

# Проверьте документацию
curl https://yourdomain.com/docs
```

## Автоматическое обновление сертификатов

### 1. Настройка cron для обновления
```bash
# Добавьте в crontab
crontab -e

# Добавьте строку для ежедневного обновления в 2:00
0 2 * * * cd /path/to/applyr && ./renew-certs.sh >> /var/log/applyr-ssl.log 2>&1
```

### 2. Ручное обновление сертификатов
```bash
# Для ручного обновления
./renew-certs.sh
```

## Мониторинг и логи

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api

# Только бот
docker-compose logs -f bot

# Только nginx
docker-compose logs -f nginx
```

### Проверка сертификатов
```bash
# Проверка срока действия сертификатов
docker-compose run --rm certbot certificates

# Проверка статуса сертификатов
docker-compose run --rm certbot certificates --show
```

## Обновление приложения

### 1. Обновление кода
```bash
# Получите последние изменения
git pull origin main

# Пересоберите и перезапустите
docker-compose down
docker-compose up -d --build
```

### 2. Обновление сертификатов
```bash
# Обновите сертификаты
./renew-certs.sh
```

## Резервное копирование

### 1. Бэкап базы данных
```bash
# Создайте бэкап
docker-compose exec postgres pg_dump -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Бэкап сертификатов
```bash
# Сертификаты автоматически сохраняются в Docker volumes
docker volume ls | grep certbot
```

## Устранение неполадок

### 1. Проблемы с SSL
```bash
# Проверьте логи certbot
docker-compose logs certbot

# Проверьте nginx конфигурацию
docker-compose exec nginx nginx -t
```

### 2. Проблемы с API
```bash
# Проверьте логи API
docker-compose logs api

# Проверьте подключение к БД
docker-compose exec api python -c "from database import AsyncSessionLocal; print('DB OK')"
```

### 3. Проблемы с ботом
```bash
# Проверьте логи бота
docker-compose logs bot

# Проверьте токен бота
docker-compose exec bot python -c "from config import app_config; print('Bot token:', app_config.TELEGRAM_BOT_TOKEN[:10] + '...')"
```

## Структура проекта

```
applyr/
├── docker-compose.yml      # Основной файл оркестрации
├── .env                    # Переменные окружения
├── init-ssl.sh            # Скрипт первоначального получения SSL
├── renew-certs.sh         # Скрипт обновления SSL
├── api/                   # Backend API
├── bot/                   # Telegram бот
└── nginx/                 # Nginx конфигурация
    ├── Dockerfile
    └── nginx.conf
```

## Преимущества данного подхода

1. **Автоматизация**: Certbot в контейнере автоматически получает и обновляет сертификаты
2. **Изоляция**: Каждый сервис работает в своем контейнере
3. **Простота**: Один `docker-compose up -d` запускает все
4. **Безопасность**: Сертификаты хранятся в Docker volumes
5. **Масштабируемость**: Легко добавить новые сервисы

## Проверка работоспособности

После деплоя проверьте:

1. **HTTPS**: `https://applyr.yourdomain.com` - должен загружаться без ошибок
2. **API**: `https://applyr.yourdomain.com/health` - должен возвращать `{"status": "healthy"}`
3. **Документация**: `https://applyr.yourdomain.com/docs` - должна открываться
4. **Telegram бот**: Отправьте `/start` - должен ответить
5. **Авторизация**: Попробуйте зарегистрироваться и войти 