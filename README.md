# Práctica Calificada 3

Este el repositorio para la tercera PC del curso de Desarrollo de Software.

### Project Structure

```
.
|-- Makefile
|-- README.md
|-- docs
|   |-- PARTE1.md
|   `-- PARTE2.md
|-- parte1
|   `-- src
|       |-- app
|       |   |-- __init__.py
|       |   |-- config.py
|       |   |-- container.py
|       |   |-- db
|       |   |   |-- __init__.py
|       |   |   |-- interfaces
|       |   |   |   |-- __init__.py
|       |   |   |   `-- db_interface.py
|       |   |   `-- session.py
|       |   |-- main.py
|       |   |-- models
|       |   |   |-- __init__.py
|       |   |   `-- user.py
|       |   |-- repositories
|       |   |   |-- interfaces
|       |   |   |   |-- __init__.py
|       |   |   |   `-- user_repository_interface.py
|       |   |   `-- user_repository.py
|       |   |-- routes
|       |   |   |-- __init__.py
|       |   |   `-- auth_router.py
|       |   |-- schemas
|       |   |   |-- __init__.py
|       |   |   `-- user.py
|       |   `-- services
|       |       |-- __init__.py
|       |       |-- auth_service.py
|       |       |-- interfaces
|       |       |   |-- __init__.py
|       |       |   |-- auth_interface.py
|       |       |   `-- token_service_interface.py
|       |       `-- jwt_service.py
|       |-- parte1.db
|       `-- tests
|           |-- __init__.py
|           |-- test_auth_router.py
|           |-- test_auth_service.py
|           |-- test_jwt_service.py
|           `-- test_user_repository.py
|-- parte1.db
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
`-- requirements.txt
```


### Requirements

Lo más importante para el proyecto es tener [Docker](https://docs.docker.com) descargado, pues el proyecto trabaja dentro de un `devcontainer`.

### Setup Configuration

La primera cosa que tienes que hacer es correr el `devcontainer`.

Una vez logré levantarse, nos apoyaremos de nuestro archivo `Makefile` para facilitarnos la ejecución de comandos.

#### Parte 1
Para correr la aplicación de FastAPI, debemos encontranos en el directorio raíz definido en el Dockerfile que inició el devcontainer `pc3`.

```
make run1
```

Para correr las pruebas de la parte:

```
make test1
```

El análisis de la parte 1 está [aquí](./docs/PARTE1.md)

#### Parte 2
Para correr la aplicación de monitoreo usando la librería `watchdogs` que ya implementa un Observer, para monitorear directorios, el cual nos ayudará a implementar nuestro patrón Observador con dos suscriptores (el de la base de datos y el logger), de igual forma, debemos encontranos en el directorio raíz definido en el Dockerfile que inició el devcontainer `pc3`.

```
make run2
```

Para correr las pruebas de la parte:

```
make test2
```

El análisis de la parte 2 está [aquí](./docs/PARTE2.md)
