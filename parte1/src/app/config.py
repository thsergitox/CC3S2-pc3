from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Clase de configuración que utiliza pydantic_settings.

    Esta configuración está diseñada para funcionar con Docker.

    Atributos:
        DATABASE_URL: (str): La URL de conexión a la base de datos SQLite.
            En un entorno Docker, esto generalmente apunta al servicio de SQLite definido en docker-compose.
    """

    # Lo ideal sería que estos valores se carguen desde variables de entorno, pero para simplificar, los valores se definen aquí.
    MONGO_URL: str
    SALT_ROUNDS: int = 10
    JWT_SECRET_KEY: str = "este_es_un_secreto_para_la_parte1"


# Instancia de la clase Settings para acceder a la configuración
settings = Settings()
