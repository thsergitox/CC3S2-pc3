import os
from app.monitor import DirectoryMonitor

def main():
    target_path = os.path.join(os.path.dirname(__file__), 'target')
    
    # Creamos el directorio target en caso no exista
    os.makedirs(target_path, exist_ok=True)
    
    monitor = DirectoryMonitor(target_path)
    
    try:
        print(f"Starting monitoring of directory: {target_path}")
        monitor.start()
        while True:
            # Mantenemos corriendo la app
            pass
    except KeyboardInterrupt:
        monitor.stop()
        print("\nMonitoring stopped")

if __name__ == "__main__":
    main()