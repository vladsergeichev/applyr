#!/bin/bash

# Скрипт для запуска тестов

echo "Запуск тестов..."

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "Ошибка: main.py не найден. Запустите скрипт из директории api/"
    exit 1
fi

# Устанавливаем переменные окружения для тестов
export PYTHONPATH=/app
export TESTING=true

# Запускаем тесты
echo "Запуск pytest..."
pytest tests/ -v --tb=short

echo "Тесты завершены." 