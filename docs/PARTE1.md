## Explicación de la parte 1

Para desarrollar el ejercicio 2 de presente parte he decidido codificar una aplicación de FastApi + SQLAlchemy con sqlite para priorizar la agilidad, para este sistema de autenticación con JWT, cuya estructura finalizó así:

```
.
`-- src
    |-- app
    |   |-- __init__.py
    |   |-- config.py
    |   |-- container.py
    |   |-- db
    |   |   |-- __init__.py
    |   |   |-- interfaces
    |   |   |   |-- __init__.py
    |   |   |   `-- db_interface.py
    |   |   `-- session.py
    |   |-- main.py
    |   |-- models
    |   |   |-- __init__.py
    |   |   `-- user.py
    |   |-- repositories
    |   |   |-- interfaces
    |   |   |   |-- __init__.py
    |   |   |   `-- user_repository_interface.py
    |   |   `-- user_repository.py
    |   |-- routes
    |   |   |-- __init__.py
    |   |   `-- auth_router.py
    |   |-- schemas
    |   |   |-- __init__.py
    |   |   `-- user.py
    |   `-- services
    |       |-- __init__.py
    |       |-- auth_service.py
    |       |-- interfaces
    |       |   |-- __init__.py
    |       |   |-- auth_interface.py
    |       |   `-- token_service_interface.py
    |       `-- jwt_service.py
    |-- parte1.db
    `-- tests
        |-- __init__.py
        |-- test_auth_router.py
        |-- test_auth_service.py
        |-- test_jwt_service.py
        `-- test_user_repository.py
```

Como se ve, se aplicaron principios SOLID, como Single Responsability, al separar nuestra API en capas como, repository, service y un controlador en `routes`, así como la Inversión de Dependencias, pues por ejemplo en `service/auth_service.py`, dependemos de abstracciones, en lugar de concreciones, inserto código:

``` py
class AuthService(AuthServiceInterface):
    # Dependemos de una interface y no de una implementación concreta
    def __init__(self, user_repository: UserRepositoryInterface, token_service: TokenServiceInterface):
        self.user_repository = user_repository
        self.token_service = token_service
```

Cumpliendo de igual manera el prinicipio de Liskov, pues en este caso, podríamos usar otra clase para el manejo de token que no sea la que se encuentra en `jwt_service.py` al Además, em todo el código.

De igual forma como se ve en la estructura, promovemos el principio de segregación de interfaces al usar interfaces en cada capa de la aplicación.

Aplicar estos principios nos ayuda a modularizar nuestro código, reduciendo el acoplamiento entre clase y aumenta su cohesión.

Esta aplicación de FastApi puede ser iniciada así

``` bash
make run1
```

Un punto a agregar, es la decición de seguir el framework para la inyección de dependencia `dependency_injector`, lo cual, fue de ayuda al momento de definir las dependencias entre las capas de la aplicación, pues facilitó este proceso.

Por otro lado, para las pruebas, las cuales ejecutamos con 

``` bash
make test1
```

Se logró cubrir 95% del código de la aplicación, el restante pertenece a el código de nuestras interfaces, por lo que logramos una alta confiabilidad de cobertura, nuestra carpeta tests, se ve algo así:

```
    `-- tests
        |-- __init__.py
        |-- test_auth_router.py
        |-- test_auth_service.py
        |-- test_jwt_service.py
        `-- test_user_repository.py
```

En `test_auth_router.py`, he decidido usar la clase de TestClient de fastapi, la cual es recomendad en su documentación [link](https://fastapi.tiangolo.com/advanced/testing-dependencies/), donde tambien se habla de la la facilidad que nos brinda para sobreescribir dependencias, por tal motivo, como nuestor interés principal es probar el comportamento de neustros endpoints, `/login` y `/register`, pues se hace un Mock de `auth_service.py`, y se sobreescribe en el container que es la clase que centraliza las dependencias,

Para `test_jwt_service.py`, simplemente se usa una instancia de la clase en si, para mirar su manejo con los tokens.

A continuación para `test_auth_service.py`, como esta clase recibe dos dependencias, en este caso el manejador de tokens, y el repositorio, para el primero usamos una instancia, pero, para el segundo mencionado, hacemos un mock para simular su comportamiento, pues lo que nos interesa es la lógica de nuestro servicio como tal.

Finalizando los test, tenemos a `test_user_repository.py`, donde he tomando la decisión de mejor hacer unos tests de integración, pues al final de cuentas es la capa que trabaja con la base de datos, y la mejor forma de probarla es asegurandonos de su comportamiento con una bd, por lo que, creamos un nuevo engine, pero trabajeremos con una bd en memoria, pues sql_alchemy, nos lo permite, como se muestra en su documentación. [Link](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/?h=memory#client-fixture), en realidad esa documentación es de SQL Model, pero me inspiré de ahí.

