from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import config

# Вариант асинхронной сессии

engine = create_async_engine(config.db.url)

async_session_maker = sessionmaker(
    engine, # движок 
    class_=AsyncSession, # 
    expire_on_commit=False) # объекты, загруженные в сессию, не должны быть удалены после фиксации транзакции

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session





# Вариант синхронной сессии
# from sqlalchemy import create_engine
# engine = create_engine(config.db.url)
# SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)
# models.Base.metadata.create_all(bind=engine)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()