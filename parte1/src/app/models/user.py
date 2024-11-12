from sqlalchemy import Column, String, CheckConstraint, Integer
from app.db.session import Base

# Definimos la clase User que hereda de Base
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    # Solo permitimos que se ingrese 'admin' o 'user' en el campo role
    __table_args__ = (
        CheckConstraint(role.in_(['admin', 'user']), name='check_role'),
    )