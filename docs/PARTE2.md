## Explicación de la parte 2

Para desarrollar el ejercicio de monitoreo de archivos, he implementado una aplicación que utiliza el patrón Observer para notificar cambios en archivos a múltiples suscriptores. La estructura del proyecto quedó así:


```
|-- parte2
|   `-- src
|       |-- app
|       |   |-- __init__.py
|       |   |-- logger.py
|       |   |-- main.py
|       |   |-- models.py
|       |   |-- monitor.py
|       |   |-- observer.py
|       |   `-- target
|       |       `-- hola.txt
|       |-- file_monitor.db
|       |-- logs
|       |   |-- file_monitor_20241112_055753.log
|       `-- tests
|           |-- __init__.py
|           `-- test_monitor.py
```


La aplicación implementa el patrón Observer de manera efectiva, donde tenemos dos suscriptores principales:

1. **DatabaseEventListener**: Guarda los eventos en SQLite.
2. **LoggingEventListener**: Registra los eventos en archivos de log.

En `observer.py`, definimos nuestras interfaces y la implementación del patrón:


Como se puede ver, seguimos los principios SOLID:
- Single Responsibility: Cada listener tiene una única responsabilidad.
- Open/Closed: Podemos agregar nuevos listeners sin modificar el código existente.
- Liskov Substitution: Cualquier nuevo listener puede reemplazar a los existentes.
- Interface Segregation: Usamos interfaces específicas para cada propósito.
- Dependency Inversion: Dependemos de abstracciones (FileEventListener) no de implementaciones.

Para las pruebas, que se encuentran en `test_monitor.py`, tomé la decisión de implementar un sistema de archivos simulado (FakeFileSystem) que nos permite:

1. Probar la creación, modificación y eliminación de archivos sin tocar el sistema real.
2. Simular eventos del sistema de archivos de manera controlada.
3. Verificar que los observers son notificados correctamente.


Donde las pruebas cubren varios escenarios críticos, tales como:
- Monitoreo de creación de archivos.
- Monitoreo de modificación de archivos.
- Monitoreo de eliminación de archivos.
- Verificación de que los eventos de directorio son ignorados.
- Pruebas de notificación a los observers.
- Manejo de errores y casos límite.


La decisión de usar un sistema de archivos simulado y mocks para las pruebas resultó en una cobertura del 83%, lo cual es muy bueno considerando la naturaleza del sistema que interactúa con recursos externos (sistema de archivos, base de datos y logs).

La aplicación puede ser iniciada con:

```
make run2
```

Y las pruebas se ejecutan con:

```
make test2
```

Un punto importante a mencionar es el uso de watchdog para el monitoreo de archivos, lo cual nos permite detectar cambios en el sistema de archivos de manera eficiente y multiplataforma. Esto, combinado con nuestro patrón Observer, nos da un sistema robusto y extensible para el monitoreo de archivos.