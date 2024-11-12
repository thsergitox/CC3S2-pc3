import jwt
from datetime import datetime, timedelta
from app.services.interfaces.token_service_interface import TokenServiceInterface

class TokenServiceJWT(TokenServiceInterface):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expiration_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def create_token(self, data: dict) -> str:
        data.update({"exp": datetime.utcnow() + timedelta(minutes=self.expiration_minutes)})
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
