from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.user import User

class AuthServiceInterface(ABC):
    @abstractmethod
    def register_user(self, db: Session, name: str, email: str, password: str, role: str) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, db: Session, email: str, password: str) -> str:
        pass
