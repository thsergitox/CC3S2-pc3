import pytest
from datetime import datetime, timedelta
import jwt
from app.services.jwt_service import TokenServiceJWT
from app.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY

# Usamos la propia la clase
@pytest.fixture
def jwt_service():
    return TokenServiceJWT(
        secret_key=JWT_SECRET_KEY,
    )

# Se siguió el patrón AAA

def test_create_token_success(jwt_service):
    # Arrange
    test_data = {"sub": "123", "role": "user"}
    
    # Act
    token = jwt_service.create_token(test_data.copy())
    
    # Assert
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == test_data["sub"]
    assert decoded["role"] == test_data["role"]
    assert "exp" in decoded

def test_create_token_includes_expiration(jwt_service):
    # Arrange
    test_data = {"sub": "123"}
    current_time = datetime.utcnow()
    
    # Act
    token = jwt_service.create_token(test_data)
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    
    # Assert
    expiration_time = datetime.fromtimestamp(decoded["exp"])
    expected_expiration = current_time + timedelta(minutes=30)
    # Allow 5 seconds tolerance for test execution time
    assert abs((expiration_time - expected_expiration).total_seconds()) < 5

def test_verify_token_success(jwt_service):
    # Arrange
    test_data = {"sub": "123", "role": "user"}
    token = jwt_service.create_token(test_data)
    
    # Act
    decoded = jwt_service.verify_token(token)
    
    # Assert
    assert decoded["sub"] == test_data["sub"]
    assert decoded["role"] == test_data["role"]

def test_verify_token_invalid_signature():
    # Arrange
    service1 = TokenServiceJWT(secret_key="key1")
    service2 = TokenServiceJWT(secret_key="key2")
    token = service1.create_token({"sub": "123"})
    
    # Act & Assert
    with pytest.raises(jwt.InvalidSignatureError):
        service2.verify_token(token)

def test_verify_token_expired():
    # Arrange
    service = TokenServiceJWT(
        secret_key="test_key",
        expiration_minutes=-1  # El token acaba ni bien se crea
    )
    token = service.create_token({"sub": "123"})
    
    # Act & Assert
    with pytest.raises(jwt.ExpiredSignatureError):
        service.verify_token(token)
