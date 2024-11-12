import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.repositories.interfaces.user_repository_interface import UserRepositoryInterface
from app.services.interfaces import TokenServiceInterface, AuthServiceInterface
from app.config import settings

SALT = bcrypt.gensalt(rounds=settings.SALT_ROUNDS)

class AuthService(AuthServiceInterface):
    # Dependemos de una interface y no de una implementación concreta
    def __init__(self, user_repository: UserRepositoryInterface, token_service: TokenServiceInterface):
        self.user_repository = user_repository
        self.token_service = token_service


    def _hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), SALT)
        return hashed_password.decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def register_user(self, user_data: UserCreateSchema) -> User:
        hashed_password = self._hash_password(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role="user",
        )
                
        
        return self.user_repository.create_user(new_user)

    def authenticate_user(self, user: UserLoginSchema) -> str:
        user_response = self.user_repository.get_by_email(user.email)
        if user_response and self._verify_password(user.password, user_response.hashed_password):
            return self.token_service.create_token({"sub": user_response.id, "role": user_response.role})
        raise ValueError("Invalid credentials")
