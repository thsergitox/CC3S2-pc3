from fastapi.testclient import TestClient
from fastapi import status
import pytest
from unittest.mock import Mock
from app.main import app
from app.container import Container
from app.schemas.user import UserCreateSchema, UserLoginSchema

client = TestClient(app)

@pytest.fixture
def mock_auth_service():
    return Mock()

@pytest.fixture
def override_container():
    container = Container()
    container.auth_service.override(Mock())
    app.container = container
    return container

@pytest.fixture
def client_with_mocked_auth(override_container):
    yield client
    app.container = Container()

def test_register_user_success(client_with_mocked_auth, override_container):
    # Arrange
    test_user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    expected_user_schema = UserCreateSchema(**test_user_data)
    
    mock_auth_service = override_container.auth_service()
    mock_auth_service.register_user.return_value = {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "role": "user"
    }

    # Act
    response = client_with_mocked_auth.post("/api/auth/register", json=test_user_data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user_data["email"]
    assert response.json()["name"] == test_user_data["name"]
    mock_auth_service.register_user.assert_called_once_with(expected_user_schema)

def test_login_user_success(client_with_mocked_auth, override_container):
    # Arrange
    test_credentials = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    expected_login_schema = UserLoginSchema(**test_credentials)
    
    mock_auth_service = override_container.auth_service()
    mock_auth_service.authenticate_user.return_value = "mocked_jwt_token"

    # Act
    response = client_with_mocked_auth.post("/api/auth/login", json=test_credentials)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"access_token": "mocked_jwt_token"}
    mock_auth_service.authenticate_user.assert_called_once_with(expected_login_schema)

def test_login_user_invalid_credentials(client_with_mocked_auth, override_container):
    # Arrange
    test_credentials = {
        "email": "wrong@example.com",
        "password": "wrongpassword"
    }
    expected_login_schema = UserLoginSchema(**test_credentials)
    
    mock_auth_service = override_container.auth_service()
    mock_auth_service.authenticate_user.side_effect = ValueError("Invalid credentials")

    # Act
    response = client_with_mocked_auth.post("/api/auth/login", json=test_credentials)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"
    mock_auth_service.authenticate_user.assert_called_once_with(expected_login_schema)