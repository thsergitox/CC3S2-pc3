from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session

class DatabaseInterface(ABC):
    """Interface for database session management"""
    
    @abstractmethod
    def create_database(self) -> None:
        """Create all database tables"""
        pass
        
    @abstractmethod
    def session(self) -> AbstractContextManager[Session]:
        """Get database session"""
        pass
