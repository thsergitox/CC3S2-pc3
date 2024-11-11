from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Clase de configuración que utiliza pydantic_settings.

    Esta configuración está diseñada para funcionar con Docker.

    Atributos:
        DATABASE_URL: (str): La URL de conexión a la base de datos SQLite.
        SALT_ROUNDS: (int): Número de rondas para el algoritmo de hashing.
        JWT_SECRET_KEY: (str): Clave secreta para firmar los tokens JWT.
    """

    # Lo ideal sería que estos valores se carguen desde variables de entorno, pero para simplificar, los valores se definen aquí.
    DATABASE_URL: str = "sqlite:///./test.db"
    SALT_ROUNDS: int = 10
    JWT_SECRET_KEY: str = "este_es_un_secreto_para_la_parte1"


# Instancia de la clase Settings para acceder a la configuración
settings = Settings()
