import logging
import os
from datetime import datetime

# Clase para manejar el logging del monitor de archivos
class FileMonitorLogger:
    def __init__(self):
        # Creamos el directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Configuramos el logger principal
        self.logger = logging.getLogger('FileMonitor')
        self.logger.setLevel(logging.INFO)
        
        # Configuramos el handler para archivo
        # El nombre del archivo incluye timestamp
        file_handler = logging.FileHandler(
            f'logs/file_monitor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler.setLevel(logging.INFO)
        
        # Configuramos el handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Creamos y aplicamos el formato de los logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Agregamos los handlers al logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_event(self, event_type: str, file_path: str):
        self.logger.info(f"File event: {event_type} - Path: {file_path}")
    
    def log_error(self, message: str):
        self.logger.error(f"Error: {message}")