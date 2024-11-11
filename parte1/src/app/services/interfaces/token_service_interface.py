from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):
    @abstractmethod
    def create_token(self, data: dict) -> str:
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass