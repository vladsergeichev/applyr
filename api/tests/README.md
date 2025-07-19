# Тесты API

## Структура тестов

```
tests/
├── __init__.py
├── conftest.py          # Конфигурация pytest и фикстуры
├── functional/          # ✅ Функциональные тесты
│   ├── __init__.py
│   ├── test_auth.py    # Тесты аутентификации
│   └── test_applies.py # Тесты откликов
└── README.md           # Документация
```

## Архитектура

### ✅ Одна БД для всего
- **PostgreSQL** - основная БД для приложения и тестов
- **Интеграционные тесты** - тестируем API через HTTP
- **Изоляция данных** - каждый тест создает уникальных пользователей
- **Простота** - одна БД проще в управлении

### 🎯 Почему одна БД оптимальна:
1. **Интеграционные тесты** - тестируем API, а не БД напрямую
2. **API изолирует данные** - уникальные пользователи в каждом тесте
3. **Меньше ресурсов** - один контейнер БД
4. **Простота конфигурации** - меньше настроек

## Список тестов

### Аутентификация (`functional/test_auth.py`)
1. **Регистрация пользователя** - `test_register_user_success`
2. **Вход пользователя** - `test_login_user_success`
3. **Рефреш токена** - `test_refresh_token_success`
4. **Выход пользователя** - `test_logout_user_success`
5. **Обработка ошибок** - тесты с неверными данными

### Отклики (`functional/test_applies.py`)
1. **Создание отклика** - `test_create_apply_success`
2. **Удаление отклика** - `test_delete_apply_success`
3. **Получение всех откликов** - `test_get_all_applies_success`
4. **Обработка ошибок** - тесты с неверными данными

## Запуск тестов

### Все функциональные тесты
```bash
docker-compose exec api python -m pytest tests/functional/ -v
```

### Тесты аутентификации
```bash
docker-compose exec api python -m pytest tests/functional/test_auth.py -v
```

### Тесты откликов
```bash
docker-compose exec api python -m pytest tests/functional/test_applies.py -v
```

### Конкретный тест
```bash
docker-compose exec api python -m pytest tests/functional/test_auth.py::test_register_user_success -v
```

## Особенности реализации

### ✅ Простые функции
- Убрали классы из тестов
- Используем простые функции с префиксом `test_`
- Фикстуры для подготовки данных

### ✅ Статус-коды
- Используем `fastapi.status` вместо магических чисел
- `status.HTTP_200_OK`, `status.HTTP_422_UNPROCESSABLE_ENTITY` и т.д.

### ✅ HTTP клиент
- Используем `requests` для HTTP запросов
- Работает с запущенным сервером
- Правильная настройка URL для контейнеров

### ✅ Уникальные данные
- Используем `uuid` для создания уникальных имен пользователей
- Избегаем конфликтов между тестами

### ✅ Одна БД
- Все тесты используют одну PostgreSQL БД
- API изолирует данные через уникальных пользователей
- Простая и надежная архитектура

## Примеры тестов

```python
def test_register_user_success(base_url):
    """Тест успешной регистрации пользователя"""
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "password": "testpass123",
        "name": "Test User"
    }
    
    response = requests.post(f"{base_url}/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
```

## Добавление новых тестов

1. Создайте функцию с префиксом `test_`
2. Используйте `fastapi.status` для статус-кодов
3. Используйте `requests` для HTTP запросов
4. Добавьте описание теста в docstring
5. Используйте уникальные данные с `uuid`
6. Размещайте тесты в папке `functional/`

## Преимущества одной БД

### ✅ Простота
- Меньше контейнеров для управления
- Проще конфигурация
- Меньше ресурсов

### ✅ Надежность
- Меньше точек отказа
- Проще отладка
- Стабильная работа

### ✅ Интеграционное тестирование
- Тестируем реальный API
- Проверяем полный стек
- Близко к продакшн среде 