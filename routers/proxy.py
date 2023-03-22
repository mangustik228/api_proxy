from fastapi import APIRouter, Depends, Body, HTTPException
from config import config
from database import get_async_session, crud, models
from sqlalchemy.orm import Session
from loguru import logger
import schema
import utils


router = APIRouter(
    prefix='/proxy',
    tags=['proxy']
)


@router.get('')
async def get_proxy(request: schema.proxy.ProxyGet = Depends(),
                    session: Session = Depends(get_async_session)):
    logger.info(f'Пришел запрос на получение прокси')
    utils.check_token(request.token)
    result = await crud.get_proxy(request, session)
    return {'status':'ok', 'data': result }


@router.post('')
async def post_proxy(request: schema.proxy.ProxyPost= Body(), 
                      session: Session = Depends(get_async_session)):
    logger.info(f'Пришел запрос на вставку прокси ({len(request.data)}шт)')
    utils.check_token(request.token)
    await crud.post_proxy(request, session)
    return HTTPException(status_code=201, detail='created')


@router.get('/full')
async def get_full_proxy(token: int, skip:int=0, count:int=100, session = Depends(get_async_session)):
    utils.check_token(token)
    result = await crud.full_proxy(session, skip, count)
    if result:
        return {'status':'ok',
                'proxies':len(result),
                'data':result}
    else: 
        raise HTTPException(status_code=204, detail='no content')

@router.delete('')
async def delete_proxy(token: int, id:int , session=Depends(get_async_session)):
    utils.check_token(token)
    result = await crud.delete_proxy(session, id)
    return {'status':result}