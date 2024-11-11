from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.interfaces.db_interface import ConnectionDBInterface
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

## Clase que implementa la interfaz de conexión a la base de datos para SQLite
class ConnectionDBSQLite(ConnectionDBInterface):
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        """Retorna una nueva sesión de la base de datos"""
        return self.SessionLocal()
