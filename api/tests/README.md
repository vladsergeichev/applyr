# Тесты API

Этот каталог содержит тесты для API приложения. Структура тестов основана на современных практиках с использованием асинхронных тестов.

## Структура

```
tests/
├── common/                 # Общие компоненты
│   ├── api_client.py      # Асинхронный API клиент
│   └── utils.py           # Утилиты для тестов
├── factories/             # Фабрики для генерации тестовых данных
│   └── base_factories.py  # Базовые фабрики с Faker
├── functional/            # Функциональные тесты
│   └── test_auth_async.py # Асинхронные тесты аутентификации
├── conftest.py            # Конфигурация pytest
└── README.md              # Этот файл
```

## Компоненты

### API Клиент

- **AsyncTestAPIClient**: Асинхронный клиент для тестирования с поддержкой ASGI

### Фабрики

- **BaseModelFactory**: Базовая фабрика с Faker для генерации тестовых данных
- **UserFactory**: Фабрика для создания данных пользователей
- **ApplyFactory**: Фабрика для создания данных откликов

### Утилиты

- Функции для генерации тестовых данных
- Функции для проверки ответов API

## Фикстуры

### Основные фикстуры

- `faker`: Экземпляр Faker для генерации данных
- `async_client`: Асинхронный API клиент
- `authorized_client`: Авторизованный клиент с токеном

### Фабрики

- `user_factory`: Фабрика пользователей
- `apply_factory`: Фабрика откликов

### Тестовые данные

- `test_user_data`: Данные пользователя
- `test_user_data_with_faker`: Данные пользователя с Faker
- `test_user_with_token`: Пользователь с токеном
- `test_apply_data`: Данные отклика
- `test_apply_data_with_faker`: Данные отклика с Faker
- `test_vacancy_data`: Данные вакансии

## Запуск тестов

### Все тесты
```bash
docker-compose exec api python -m pytest tests/ -v
```

### Только асинхронные тесты
```bash
docker-compose exec api python -m pytest tests/functional/test_auth_async.py -v
```

### Тесты с подробным выводом
```bash
docker-compose exec api python -m pytest tests/ -v -s
```

### Тесты с покрытием
```bash
docker-compose exec api python -m pytest tests/ --cov=. --cov-report=html
```

## Примеры использования

### Создание тестового пользователя
```python
async def test_example(async_client: AsyncTestAPIClient, user_factory: UserFactory):
    user_data = user_factory.build_user_data()
    response = await async_client.register_user(user_data)
    assert response.status_code == 200
```

### Использование авторизованного клиента
```python
async def test_authorized_endpoint(authorized_client: AsyncTestAPIClient):
    apply_data = {
        "name": "Test Job",
        "link": "https://example.com/job",
        "user_id": 1,
        "company_name": "Test Company",
        "description": "Test description"
    }
    response = await authorized_client.create_apply(apply_data)
    assert response.status_code == 200
```

### Использование утилит
```python
from tests.common.utils import assert_response_status, assert_response_contains

async def test_with_utils(async_client: AsyncTestAPIClient):
    response = await async_client.get("/some/endpoint")
    assert_response_status(response, 200)
    assert_response_contains(response, ["key1", "key2"])
```

## Лучшие практики

1. **Используйте асинхронные тесты** для всех новых тестов
2. **Используйте фабрики** для генерации тестовых данных
3. **Используйте утилиты** для проверки ответов
4. **Используйте фикстуры** для переиспользования данных
5. **Очищайте данные** после тестов
6. **Используйте параметризацию** для тестирования разных сценариев

## Зависимости

Для работы тестов требуются следующие зависимости:
- `pytest`
- `pytest-asyncio`
- `httpx`
- `faker`
- `asgi-lifespan` 