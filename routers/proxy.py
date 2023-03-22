from fastapi import APIRouter, Depends, Body, HTTPException
from config import config
from database import get_async_session, crud, models
from sqlalchemy.orm import Session
from loguru import logger
import schema
import utils


router = APIRouter(
    prefix='/v1',
    tags=['proxy'] 
    )


@router.get('/full')
async def get_full_proxy(token: int, skip:int=0, count:int=100, session = Depends(get_async_session)):
    utils.check_token(token)
    logger.info(f'Запрос всех данных')
    result = await crud.full_proxy(session, skip, count)
    if result:
        return {'status':'ok',
                'proxies':len(result),
                'data':result}
    else: 
        raise HTTPException(status_code=204, detail='no content')


@router.get('/')
async def get_proxies(request: schema.proxy.ProxyGet = Depends(),
                    session: Session = Depends(get_async_session)):
    '''
    Получение актуальных прокси запрос формата  
    форматы ответетов в зависимости от `type`: 

        - "string":
            "status": "ok",
            "data": [{
                "http": "http://user:pass@127.0.0.1:8000",
                "https": "https://user:pass@127.0.0.1:8000"
                },...

        - "dict[str,str]"
            "status": "ok",
            "data": [
                {
                    "server": "http://127.0.0.1:8000",
                    "username": "user",
                    "password": "pass"
                },...

        - "playwright"
            "status": "ok",
            "data": [
                {
                    "proxy": {
                        "server": "http://127.0.0.1:8000",
                        "username": "user",
                        "password": "pass"
                    }
                },...

        Параметр expire: до какого числа работает прокси(не обязательный, по умолчанию "до завтра")
    '''
    logger.info(f'Пришел запрос на получение прокси')
    utils.check_token(request.token)
    result = await crud.get_proxy(request, session)
    return {'status':'ok', 'data': result }


@router.post('/')
async def post_proxies(request: schema.proxy.ProxyPost= Body(), 
                      session: Session = Depends(get_async_session)):
    '''
    `service`: не обязательный параметр  
    `expire`: До какого числа прокси. формат даты: 2022-03-30
    
    '''
    logger.info(f'Пришел запрос на вставку прокси ({len(request.data)}шт)')
    utils.check_token(request.token)
    await crud.post_proxy(request, session)
    return HTTPException(status_code=201, detail='created')


@router.delete('/')
async def delete_proxy(token: int, id:int , session=Depends(get_async_session)):
    '''Удалить прокси по id'''
    logger.info(f'Запрос на удаление прокси {id}')
    utils.check_token(token)
    result = await crud.delete_proxy(session, id)
    return {'status':result}


@router.put('/')
async def update_proxy(token: int,
                       request: schema.proxy.ProxyUpdate = Body(),
                       session=Depends(get_async_session)):
    '''Обновить прокси по id,
    token и id необходимо указать в query-string url
    
    Информация прикладывать json в тело запроса
    '''
    logger.info(f'Запрос на обновление прокси {request.id}')
    utils.check_token(token)
    result = await crud.update_proxy(session, request)
    return {'status':result}