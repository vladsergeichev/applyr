#!/bin/bash

# Скрипт для очистки базы данных
# Удаляет все таблицы и данные

echo "🧹 Очистка базы данных..."

# Проверяем, что контейнеры запущены
if ! docker-compose ps | grep -q "postgres.*Up"; then
    echo "❌ PostgreSQL контейнер не запущен. Запустите docker-compose up -d"
    exit 1
fi

# Выполняем SQL скрипт очистки
echo "🗑️  Удаляем все таблицы..."
docker-compose exec -T postgres psql -U postgres -d applyr < scripts/clear_db.sql

if [ $? -eq 0 ]; then
    echo "✅ База данных успешно очищена!"
    echo "📊 Текущие таблицы в базе данных:"
    docker-compose exec postgres psql -U postgres -d applyr -c "\dt"
else
    echo "❌ Ошибка при очистке базы данных"
    exit 1
fi 