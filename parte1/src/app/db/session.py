from contextlib import contextmanager
from typing import Generator
import logging
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.db.interfaces.db_interface import DatabaseInterface

# Configuración del logger para este módulo
logger = logging.getLogger(__name__)

# Clase base para los modelos SQLAlchemy
Base = declarative_base()

# Clase que maneja la sesion a la base de datos, es un singleton
class SessionLocal(DatabaseInterface):

    def __init__(self, db_url: str) -> None:
        # Inicializa el motor de base de datos con la URL proporcionada
        self._engine = create_engine(db_url, echo=True)
        # Crea una fábrica de sesiones con scope
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,  # No hacer commit automático
                autoflush=False,   # No hacer flush automático
                bind=self._engine, # Vincula al motor creado
            ),
        )

    def create_database(self) -> None:
        # Crea todas las tablas definidas en los modelos
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        # Crea una nueva sesión de base de datos
        session: Session = self._session_factory()
        try:
            # Cede la sesión al contexto
            yield session
        except Exception:
            # En caso de error, hace rollback de la sesión
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            # Siempre cierra la sesión al finalizar
            session.close()