from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler  
from .observer import Subject, DatabaseEventListener, LoggingEventListener  
from .logger import FileMonitorLogger 

# Clase que maneja los eventos de cambios en archivos
# Hereda de FileSystemEventHandler para detectar eventos del sistema de archivos
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, subject: Subject):
        self.subject = subject
        self.logger = FileMonitorLogger()

    # Se ejecuta cuando se crea un nuevo archivo
    def on_created(self, event):
        if not event.is_directory:  # Solo procesamos archivos, no directorios
            self.subject.notify('created', event.src_path)

    # Se ejecuta cuando se modifica un archivo
    def on_modified(self, event):
        if not event.is_directory:
            self.subject.notify('modified', event.src_path)

    # Se ejecuta cuando se elimina un archivo
    def on_deleted(self, event):
        if not event.is_directory:
            self.subject.notify('deleted', event.src_path)

# Clase principal que maneja el monitoreo del directorio
class DirectoryMonitor:
    def __init__(self, path: str):
        self.path = path  # Ruta del directorio a monitorear
        self.logger = FileMonitorLogger()
        self.subject = Subject()  # Creamos el subject del patrón observer
        
        # Registramos los observers para base de datos y logging
        self.subject.attach(DatabaseEventListener())
        self.subject.attach(LoggingEventListener())
        
        # Configuramos el manejador de eventos y el observer
        self.event_handler = FileChangeHandler(self.subject)
        self.observer = Observer()

    # Método para iniciar el monitoreo
    def start(self):
        try:
            self.observer.schedule(self.event_handler, self.path, recursive=False)
            self.observer.start()
            self.logger.log_event("monitor_start", self.path)
        except Exception as e:
            self.logger.log_error(f"Failed to start monitor: {str(e)}")

    # Método para detener el monitoreo
    def stop(self):
        try:
            self.observer.stop()
            self.observer.join()
            self.logger.log_event("monitor_stop", self.path)
        except Exception as e:
            self.logger.log_error(f"Failed to stop monitor: {str(e)}")