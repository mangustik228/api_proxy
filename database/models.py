from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
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

    __table_args__ = (UniqueConstraint(
        'username', 
        'password',
        'port',
        'server',
        'expire', 
        name='unique_value'),)