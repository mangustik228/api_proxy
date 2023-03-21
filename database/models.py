from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

__all__ = ['Proxy']


Base = declarative_base()

class Proxy(Base):
    __tablename__='proxy'
    
    id = Column(Integer, primary_key=True, index=True)
    create = Column(DateTime, default=datetime.utcnow())
    server = Column(String)
    username = Column(String)
    password = Column(String)
    port = Column(Integer)
    expire = Column(DateTime)
    service = Column(String, nullable=True)
