import pytest
from unittest.mock import Mock  # Mock es un spy
from app.services.auth_service import AuthService
from app.services.jwt_service import TokenServiceJWT
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY

# Mock del repositorio de usuarios para simular la capa de persistencia
@pytest.fixture
def mock_user_repository():
    return Mock()  # Mock/Spy: Se usa un Mock para simular el comportamiento del repositorio

# Servicio real de tokens JWT 
@pytest.fixture
def token_service():
    return TokenServiceJWT(secret_key=JWT_SECRET_KEY)  # Se usa el servicio real (no es un mock)

# Servicio de autenticación con sus dependencias
@pytest.fixture
def auth_service(mock_user_repository, token_service):
    return AuthService(
        user_repository=mock_user_repository,
        token_service=token_service
    )

# Se siguió el patrón AAA

def test_register_user_success(auth_service, mock_user_repository):
    # Prueba el registro exitoso de un usuario
    # Arrange
    test_user_data = UserCreateSchema(
        name="Test User",
        email="test@example.com",
        password="testpassword"
    )
    
    # Mock/Spy: Se configura el comportamiento esperado del repositorio
    mock_user_repository.create_user.return_value = User(
        id=1,
        name="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        role="user"
    )

    # Act
    result = auth_service.register_user(test_user_data)

    # Assert
    assert result.name == test_user_data.name
    assert result.email == test_user_data.email
    assert result.role == "user"
    mock_user_repository.create_user.assert_called_once()  # Mock/Spy: Verifica que el mock fue llamado una vez

def test_authenticate_user_success(auth_service, mock_user_repository):
    # Prueba la autenticación exitosa de un usuario
    # Arrange
    test_credentials = UserLoginSchema(
        email="test@example.com",
        password="testpassword"
    )
    
    # Mock/Spy: Se crea un usuario simulado con contraseña conocida
    hashed_password = auth_service._hash_password("testpassword")
    mock_user = User(
        id=1,
        name="Test User",
        email="test@example.com",
        hashed_password=hashed_password,
        role="user"
    )
    
    # Mock/Spy: Se configura el comportamiento del repositorio
    mock_user_repository.get_by_email.return_value = mock_user

    # Act
    token = auth_service.authenticate_user(test_credentials)

    # Assert
    assert isinstance(token, str)
    mock_user_repository.get_by_email.assert_called_once_with(test_credentials.email)  # Mock/Spy: Verifica la llamada

def test_authenticate_user_invalid_password(auth_service, mock_user_repository):
    # Prueba el caso de autenticación con contraseña inválida
    # Arrange
    test_credentials = UserLoginSchema(
        email="test@example.com",
        password="wrongpassword"
    )
    
    # Mock/Spy: Se crea un usuario simulado con contraseña diferente
    hashed_password = auth_service._hash_password("testpassword")
    mock_user = User(
        id=1,
        name="Test User",
        email="test@example.com",
        hashed_password=hashed_password,
        role="user"
    )
    
    # Mock/Spy: Se configura el comportamiento del repositorio
    mock_user_repository.get_by_email.return_value = mock_user

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        auth_service.authenticate_user(test_credentials)

def test_authenticate_user_nonexistent_user(auth_service, mock_user_repository):
    # Prueba el caso de autenticación con usuario inexistente
    # Arrange
    test_credentials = UserLoginSchema(
        email="nonexistent@example.com",
        password="testpassword"
    )
    
    # Mock/Spy: Se simula que no se encuentra el usuario
    mock_user_repository.get_by_email.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials"):
        auth_service.authenticate_user(test_credentials)
