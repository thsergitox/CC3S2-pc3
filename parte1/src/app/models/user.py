from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Definimos la clase User que hereda de Base
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, index=True)
    
    # Solo permitimos que se ingrese 'admin' o 'user' en el campo role
    __table_args__ = (
        CheckConstraint(role.in_(['admin', 'user']), name='check_role'),
    )