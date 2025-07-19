import pytest
import requests
import uuid
from fastapi import status


@pytest.fixture
def base_url():
    """Базовый URL для API"""
    return "http://api:8000"


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
    assert data["token_type"] == "bearer"


def test_register_user_missing_fields(base_url):
    """Тест регистрации с отсутствующими полями"""
    user_data = {
        "username": "testuser"
        # Отсутствуют password и name
    }
    
    response = requests.post(f"{base_url}/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_user_success(base_url):
    """Тест успешного входа пользователя"""
    # Сначала регистрируем пользователя
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "password": "testpass123",
        "name": "Test User"
    }
    requests.post(f"{base_url}/auth/register", json=user_data)
    
    # Теперь входим
    login_data = {
        "username": unique_username,
        "password": "testpass123"
    }
    
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(base_url):
    """Тест входа с неверными учетными данными"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token_success(base_url):
    """Тест успешного обновления токена"""
    # Регистрируем пользователя
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "password": "testpass123",
        "name": "Test User"
    }
    register_response = requests.post(f"{base_url}/auth/register", json=user_data)
    register_data = register_response.json()
    
    # Проверяем, есть ли refresh_token в ответе
    if "refresh_token" not in register_data:
        pytest.skip("API doesn't return refresh_token")
    
    # Обновляем токен
    refresh_data = {
        "refresh_token": register_data["refresh_token"]
    }
    
    response = requests.post(f"{base_url}/auth/refresh", json=refresh_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data


def test_refresh_token_invalid(base_url):
    """Тест обновления с недействительным токеном"""
    refresh_data = {
        "refresh_token": "invalid_token"
    }
    
    response = requests.post(f"{base_url}/auth/refresh", json=refresh_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_user_success(base_url):
    """Тест успешного выхода пользователя"""
    # Регистрируем пользователя
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "username": unique_username,
        "password": "testpass123",
        "name": "Test User"
    }
    register_response = requests.post(f"{base_url}/auth/register", json=user_data)
    register_data = register_response.json()
    
    # Проверяем, есть ли refresh_token в ответе
    if "refresh_token" not in register_data:
        pytest.skip("API doesn't return refresh_token")
    
    # Выходим
    logout_data = {
        "refresh_token": register_data["refresh_token"]
    }
    
    response = requests.post(f"{base_url}/auth/logout", json=logout_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Успешный выход" 