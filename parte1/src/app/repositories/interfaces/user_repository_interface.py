from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepositoryInterface(ABC):

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass
