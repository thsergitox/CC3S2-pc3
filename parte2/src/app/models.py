from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Declaramos nuestra tabala que guardará los eventos que nuestro observer notificará
class FileEvent(Base):
    __tablename__ = 'file_events'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    file_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Creamos una sesion de base datos
engine = create_engine('sqlite:///file_monitor.db')
# Creamos la tabla file_events en caso no exista
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)