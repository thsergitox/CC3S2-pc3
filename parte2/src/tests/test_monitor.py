import pytest
import os
import tempfile
from unittest.mock import Mock
from app.monitor import DirectoryMonitor
from app.models import Session, FileEvent, Base
from app.observer import DatabaseEventListener, LoggingEventListener
from sqlalchemy import create_engine

# Clase para simular un sistema de archivos en memoria para pruebas
class FakeFileSystem:
    def __init__(self, base_path):
        self.base_path = base_path
        self.files = {}

    def create_file(self, filename, content=""):
        path = os.path.join(self.base_path, filename)
        self.files[path] = content
        return path

    def modify_file(self, filename, content):
        path = os.path.join(self.base_path, filename)
        self.files[path] = content
        return path

    def delete_file(self, filename):
        path = os.path.join(self.base_path, filename)
        if path in self.files:
            del self.files[path]
        return path

@pytest.fixture
def fake_db():
    # Creamos nuevamente una base de datos SQLite en memoria para pruebas
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    return engine

@pytest.fixture
def fake_fs():
    # Crearmos un directorio temporal y sistema de archivos simulado
    with tempfile.TemporaryDirectory() as temp_dir:
        yield FakeFileSystem(temp_dir)

def test_file_creation_monitoring(fake_db, fake_fs):
    # Arrange: Usamos el FakeFileSystem para simular la creación de archivos sin tocar el sistema real
    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.start()

    # Act: Creamos un archivo de prueba usando el sistema de archivos simulado
    file_path = fake_fs.create_file("test.txt", "test content")

    # Simulamos evento del sistema de archivos usando Mock
    event = Mock()
    event.src_path = file_path
    event.is_directory = False
    monitor.event_handler.on_created(event)

    # Assert: Verificamos entrada en base de datos
    session = Session()
    event_record = session.query(FileEvent).filter_by(event_type="created").first()
    
    assert event_record is not None
    assert event_record.file_path == file_path
    assert event_record.event_type == "created"
    
    monitor.stop()
    session.close()

def test_file_modification_monitoring(fake_db, fake_fs):
    # Arrange: Usamos el FakeFileSystem para simular modificaciones de archivos
    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.start()

    # Act: Crear y modificar un archivo de prueba
    file_path = fake_fs.create_file("test.txt", "initial content")
    fake_fs.modify_file("test.txt", "modified content")

    # Simular evento de modificación
    event = Mock()
    event.src_path = file_path
    event.is_directory = False
    monitor.event_handler.on_modified(event)

    # Assert: Verificamos entrada en base de datos
    session = Session()
    event_record = session.query(FileEvent).filter_by(event_type="modified").first()
    
    assert event_record is not None
    assert event_record.file_path == file_path
    assert event_record.event_type == "modified"
    
    monitor.stop()
    session.close()

def test_file_deletion_monitoring(fake_db, fake_fs):
    # Arrange: Usamos el FakeFileSystem para simular eliminación de archivos
    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.start()

    # Act: Creamos y eliminar un archivo de prueba
    file_path = fake_fs.create_file("test.txt")
    fake_fs.delete_file("test.txt")

    # Simulamos evento de eliminación
    event = Mock()
    event.src_path = file_path
    event.is_directory = False
    monitor.event_handler.on_deleted(event)

    # Assert: Verificamos la entrada en base de datos
    session = Session()
    event_record = session.query(FileEvent).filter_by(event_type="deleted").first()
    
    assert event_record is not None
    assert event_record.file_path == file_path
    assert event_record.event_type == "deleted"
    
    monitor.stop()
    session.close()

def test_directory_events_ignored(fake_db, fake_fs):
    # Arrange: Verificamos que los eventos de directorio son ignorados
    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.start()

    # Act: Simulamos evento de directorio
    event = Mock()
    event.src_path = os.path.join(fake_fs.base_path, "test_dir")
    event.is_directory = True
    
    monitor.event_handler.on_created(event)
    monitor.event_handler.on_modified(event)
    monitor.event_handler.on_deleted(event)

    # Assert: Verificamos que no hay entradas en la base de datos para eventos de directorio
    session = Session()
    events_count = session.query(FileEvent).count()
    
    assert events_count == 0
    
    monitor.stop()
    session.close()

@pytest.mark.parametrize("event_type", ["created", "modified", "deleted"])
def test_observer_notification(fake_fs, event_type):
    # Arrange: Usamos Mock para verificar que los observadores son notificados correctamente
    mock_db_listener = Mock(spec=DatabaseEventListener)
    mock_log_listener = Mock(spec=LoggingEventListener)

    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.subject._observers = [mock_db_listener, mock_log_listener]
    monitor.start()

    # Act: Simulamos evento de archivo
    file_path = fake_fs.create_file("test.txt")
    event = Mock()
    event.src_path = file_path
    event.is_directory = False

    # Activamos el manejador de eventos apropiado
    event_handler = getattr(monitor.event_handler, f"on_{event_type}")
    event_handler(event)

    # Assert: Verificamos que ambos observadores fueron notificados
    mock_db_listener.update.assert_called_once_with(event_type, file_path)
    mock_log_listener.update.assert_called_once_with(event_type, file_path)

    monitor.stop()

def test_monitor_stop_not_running(fake_db, fake_fs):
    # Arrange: Inicializamos el monitor
    monitor = DirectoryMonitor(fake_fs.base_path)
    
    # Act: Intentamos detener cuando no está en ejecución
    monitor._is_running = False
    monitor.stop()
    
    # Assert: Verificamos que no se registró ningún evento de detención
    session = Session()
    stop_events = session.query(FileEvent).filter_by(event_type="monitor_stop").count()
    assert stop_events == 0
    session.close()

def test_monitor_stop_failure(fake_db, fake_fs):
    # Arrange: Inicializamos el monitor y lo arrancamos
    monitor = DirectoryMonitor(fake_fs.base_path)
    monitor.start()
    
    # Mockeamos observer.stop() para que lance una excepción
    def mock_stop():
        raise Exception("Failed to stop observer")
    
    monitor.observer.stop = mock_stop
    monitor._is_running = True
    
    # Act: Intentamos detener con fallo simulado
    try:
        monitor.stop()
    except Exception as e:
        # Assert: Verificamos que la excepción es la esperada
        assert str(e) == "Failed to stop observer"
    
    # Assert: Verificamos que el monitor sigue marcado como en ejecución
    assert monitor._is_running