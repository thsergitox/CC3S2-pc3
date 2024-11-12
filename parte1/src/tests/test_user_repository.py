# Importaciones necesarias para las pruebas
import pytest
from sqlalchemy import create_engine
from app.db.session import Base, SessionLocal
from app.repositories.user_repository import UserRepository
from app.models.user import User

# URL de la base de datos de prueba usando SQLite en memoria
# Se podría considerar un stub ?
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    # Crea la base de datos y sesión de prueba
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    # Crea una sesión local para las pruebas
    session_local = SessionLocal(db_url=TEST_DATABASE_URL)
    session_local.create_database()
    yield session_local
    
    # Limpia la base de datos después de las pruebas
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user_repository(test_db):
    # Crea una instancia del repositorio de usuarios para las pruebas
    return UserRepository(db=test_db.session)

def test_create_user(user_repository):
    # Prueba la creación exitosa de un usuario
    # Arrange: Prepara los datos de prueba
    test_user = User(
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpass123",
        role="user"
    )
    
    # Act: Ejecuta la acción de crear usuario
    created_user = user_repository.create_user(test_user)
    
    # Assert: Verifica que el usuario se creó correctamente
    assert created_user.id is not None
    assert created_user.name == test_user.name
    assert created_user.email == test_user.email
    assert created_user.role == "user"

def test_get_user_by_email(user_repository):
    # Prueba la búsqueda de usuario por email
    # Arrange: Crea un usuario de prueba
    test_user = User(
        name="Test Get User",
        email="test_get@example.com",
        hashed_password="hashedpass123",
        role="user"
    )
    user_repository.create_user(test_user)
    
    # Act: Busca el usuario por email
    found_user = user_repository.get_by_email("test_get@example.com")
    
    # Assert: Verifica que se encontró el usuario correcto
    assert found_user is not None
    assert found_user.email == test_user.email
    assert found_user.name == test_user.name

def test_get_user_by_id(user_repository):
    # Prueba la búsqueda de usuario por ID
    # Arrange: Crea un usuario de prueba
    test_user = User(
        name="Test Get By ID",
        email="test_get_id@example.com",
        hashed_password="hashedpass123",
        role="user"
    )
    created_user = user_repository.create_user(test_user)
    
    # Act: Busca el usuario por ID
    found_user = user_repository.get_by_id(str(created_user.id))
    
    # Assert: Verifica que se encontró el usuario correcto
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == test_user.email

def test_get_nonexistent_user_by_email(user_repository):
    # Prueba la búsqueda de un usuario que no existe por email
    # Act: Intenta buscar un usuario con email inexistente
    found_user = user_repository.get_by_email("nonexistent@example.com")
    
    # Assert: Verifica que no se encontró ningún usuario
    assert found_user is None

def test_get_nonexistent_user_by_id(user_repository):
    # Prueba la búsqueda de un usuario que no existe por ID
    # Act: Intenta buscar un usuario con ID inexistente
    found_user = user_repository.get_by_id("999")
    
    # Assert: Verifica que no se encontró ningún usuario
    assert found_user is None

def test_create_user_with_duplicate_email(user_repository):
    # Prueba que no se puede crear un usuario con un email duplicado
    # Arrange: Crea un primer usuario
    test_user1 = User(
        name="Test User 1",
        email="duplicate@example.com",
        hashed_password="hashedpass123",
        role="user"
    )
    user_repository.create_user(test_user1)
    
    # Intenta crear un segundo usuario con el mismo email
    test_user2 = User(
        name="Test User 2",
        email="duplicate@example.com",
        hashed_password="hashedpass456",
        role="user"
    )
    
    # Act & Assert: Verifica que se lanza una excepción al intentar crear el usuario duplicado
    with pytest.raises(Exception):  # SQLite lanzará un IntegrityError
        user_repository.create_user(test_user2)
