# Práctica Califica 3

Este el repositorio para la tercera PC del curso de Desarrollo de Software.

### Project Structure

```
.
|-- Makefile
|-- README.md
|-- ov=parte1
|   `-- src
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
|-- parte2
|   `-- src
|       |-- app
|       |   `-- __init__.py
|       `-- tests
|           `-- __init__.py
`-- requirements.txt
```


### Requirements

Lo más importante para el proyecto es tener [Docker](https://docs.docker.com) descargado, pues el proyecto trabaja dentro de un `devcontainer`.

### Setup Configuration

La primera cosa que tienes que hacer es correr el `devcontainer`.

Una vez logré levantarse, nos apoyaremos de nuestro archivo `Makefile` para facilitarnos la ejecución de comandos.

#### Parte 1
Para correr la aplicación de FastAPI:

```
make run1
```

Para correr las pruebas de la parte:

```
make test1
```
