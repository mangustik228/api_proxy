from loguru import logger
from sqlalchemy import select, delete
import schema
from sqlalchemy.ext.asyncio import AsyncSession
from database import models
from fastapi import HTTPException

async def get_proxy(request: schema.proxy.ProxyGet, session: AsyncSession):
    logger.debug(f'request = \n{request}')
    query = select(models.Proxy)\
        .where(models.Proxy.expire > request.expire)
    proxies = await session.execute(query)
    proxies = proxies.all()
    proxy_schema = [schema.proxy.ProxyGetResponse.from_orm(proxy.Proxy) for proxy in proxies]
    if not proxy_schema:
        raise HTTPException(status_code=204, detail='no content')
    if request.type == 'string':
        return [proxy.string_val() for proxy in proxy_schema]
    elif request.type == 'dict[str,str]':
        return [proxy.dict_str_str() for proxy in proxy_schema]
    else: # request.type == 'playwright'
        return [proxy.dict_playwright() for proxy in proxy_schema]


async def post_proxy(request: schema.proxy.ProxyPost, session: AsyncSession):
    logger.info(request)
    data = [models.Proxy(**item.dict()) for item in request.data]
    session.add_all(data)
    await session.commit()


async def full_proxy(session: AsyncSession, skip, count):
    query = select(models.Proxy).offset(skip).limit(count)
    result = await session.execute(query)
    return result.all()

async def delete_proxy(session: AsyncSession, id:int):
    query = select(models.Proxy).where(models.Proxy.id == id)
    result = await session.execute(query)
    if not result.fetchall():
        logger.info(f'Попытка удалить прокси второй раз')
        return 'proxy уже был удален'
    stmt = delete(models.Proxy).where(models.Proxy.id == id)
    await session.execute(stmt)
    await session.commit()
    logger.info(f'Удален прокси с id={id}')
    return 'ok'