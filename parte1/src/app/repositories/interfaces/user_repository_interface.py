from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, user_id: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> User:
        pass

    @abstractmethod
    def create_user(self, db: Session, user: User) -> User:
        pass
