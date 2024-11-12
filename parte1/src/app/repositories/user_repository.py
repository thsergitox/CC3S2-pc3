from sqlalchemy.orm import Session
from typing import Callable
from contextlib import AbstractContextManager

from app.models.user import User
from app.repositories.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):   

    # Trabajar por inyección a la base de datos nos ayudará para los test de integración
    def __init__(self, db: Callable[..., AbstractContextManager[Session]]):
        self.db = db

    # Inyectamos la sesion a la base de datos
    def get_by_id(self, user_id: str) -> User:
        with self.db() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User:
        with self.db() as session:
            return session.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        with self.db() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
