from fastapi import APIRouter, Query, Depends, HTTPException, Body, Path
from sqlalchemy import insert, select
from config import config
from database import get_async_session, crud, models
from sqlalchemy.orm import Session
from loguru import logger
import schema


router = APIRouter(
    prefix='/proxy',
    tags=['proxy']
)


@router.get('')
async def get_proxy(request: schema.proxy.ProxyGet = Depends(),
                    session: Session = Depends(get_async_session)):
    logger.info(f'Пришел запрос на получение прокси')
    if request.token != config.token:
        return HTTPException(status_code=401, detail="your token - is bullshit")
    result = await crud.get_proxy(request, session)
    if not result:
        return {'status':'empty'}
    else:
        return {'status':'ok', 'data': result }

@router.post('')
async def post_proxy(request: schema.proxy.ProxyPost= Body(), 
                      session: Session = Depends(get_async_session)):
    logger.info(f'Пришел запрос на вставку прокси')
    if request.token != config.token: 
        logger.info(f'Не правильный токен')
        return HTTPException(status_code=401, detail="your token - is bullshit")
    stmt = insert(models.Proxy).values(request.data.dict())
    await session.execute(stmt) 
    await session.commit() 
    return {'status': 'success'}