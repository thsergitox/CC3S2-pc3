from dependency_injector import containers, providers

from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.jwt_service import TokenServiceJWT
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
JWT_SECRET_KEY = settings.JWT_SECRET_KEY

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["app.routes.auth_router"])

    db = providers.Singleton(SessionLocal, db_url=DATABASE_URL)

    user_repository = providers.Factory(
        UserRepository,
        db=db.provided.session,
    )

    jwt_service = providers.Factory(
        TokenServiceJWT,
        secret_key=JWT_SECRET_KEY       
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository,
        token_service=jwt_service
    )