from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class ConnectionDBInterface(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        """Obtiene una nueva sesión de la base de datos"""
        pass
