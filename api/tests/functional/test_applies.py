import pytest
import requests
import uuid
from fastapi import status


@pytest.fixture
def base_url():
    """Базовый URL для API"""
    return "http://api:8000"


@pytest.fixture
def auth_headers(base_url):
    """Создает заголовки авторизации"""
    # Регистрируем пользователя
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "password": "testpass123",
        "name": "Test User"
    }
    response = requests.post(f"{base_url}/auth/register", json=user_data)
    token_data = response.json()
    
    return {"Authorization": f"Bearer {token_data['access_token']}"}


def test_create_apply_success(base_url, auth_headers):
    """Тест успешного создания отклика"""
    apply_data = {
        "user_id": 123456789,
        "name": "Python Developer",
        "link": "https://example.com/job",
        "company_name": "Test Company",
        "description": "Test job description"
    }
    
    response = requests.post(f"{base_url}/applies/create_apply", json=apply_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == apply_data["user_id"]
    assert data["name"] == apply_data["name"]
    assert data["link"] == apply_data["link"]


def test_create_apply_missing_required_fields(base_url, auth_headers):
    """Тест создания отклика с отсутствующими обязательными полями"""
    apply_data = {
        "user_id": 123456789
        # Отсутствуют name и link
    }
    
    response = requests.post(f"{base_url}/applies/create_apply", json=apply_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_apply_success(base_url, auth_headers):
    """Тест успешного удаления отклика"""
    # Сначала создаем отклик
    apply_data = {
        "user_id": 123456789,
        "name": "Python Developer",
        "link": "https://example.com/job",
        "company_name": "Test Company",
        "description": "Test job description"
    }
    create_response = requests.post(f"{base_url}/applies/create_apply", json=apply_data, headers=auth_headers)
    apply_id = create_response.json()["id"]
    
    # Удаляем отклик
    response = requests.delete(f"{base_url}/applies/delete_apply/{apply_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Отклик успешно удален"


def test_delete_apply_nonexistent(base_url, auth_headers):
    """Тест удаления несуществующего отклика"""
    response = requests.delete(f"{base_url}/applies/delete_apply/999", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_applies_success(base_url, auth_headers):
    """Тест успешного получения всех откликов"""
    # Создаем отклик
    apply_data = {
        "user_id": 123456789,
        "name": "Python Developer",
        "link": "https://example.com/job",
        "company_name": "Test Company",
        "description": "Test job description"
    }
    requests.post(f"{base_url}/applies/create_apply", json=apply_data, headers=auth_headers)
    
    # Получаем все отклики
    response = requests.get(f"{base_url}/applies/get_applies/testuser", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == apply_data["name"]


def test_get_all_applies_empty(base_url, auth_headers):
    """Тест получения откликов для пользователя без откликов"""
    response = requests.get(f"{base_url}/applies/get_applies/testuser", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0 