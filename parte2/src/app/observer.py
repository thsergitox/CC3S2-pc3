from abc import ABC, abstractmethod
from typing import List
from app.models import Session, FileEvent
from app.logger import FileMonitorLogger

# Clase base abstracta para los listeners de eventos
class FileEventListener(ABC):
    @abstractmethod
    def update(self, event_type: str, file_path: str):
        pass

# Sucriptor/Listener que guarda los eventos en la base de datos
class DatabaseEventListener(FileEventListener):
    def __init__(self):
        self.logger = FileMonitorLogger()

    def update(self, event_type: str, file_path: str):
        try:
            # Creamos una nueva sesión de BD
            session = Session()
            # Creamos y guardamos el evento
            event = FileEvent(event_type=event_type, file_path=file_path)
            session.add(event)
            session.commit()
            self.logger.log_event(event_type, file_path)
            session.close()
        except Exception as e:
            self.logger.log_error(f"Database error: {str(e)}")


# Supscritor Listener que registra los eventos en el log
class LoggingEventListener(FileEventListener):
    def __init__(self):
        self.logger = FileMonitorLogger()

    def update(self, event_type: str, file_path: str):
        self.logger.log_event(event_type, file_path)


# Implementamos del patrón Observer
class Subject:
    def __init__(self):
        self._observers: List[FileEventListener] = []  # Lista de observadores

    # Método para agregar un nuevo listener
    def attach(self, observer: FileEventListener):
        self._observers.append(observer)

    # Método para notificar a nuestros suscribers ante un evento
    def notify(self, event_type: str, file_path: str):
        for observer in self._observers:
            observer.update(event_type, file_path)