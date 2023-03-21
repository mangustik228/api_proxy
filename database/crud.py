import json
from loguru import logger
from sqlalchemy import select
import schema
from sqlalchemy.orm import Session
from database import models

async def get_proxy(request: schema.proxy.ProxyGet, session: Session):
    logger.debug(f'request = \n{request}')
    query = select(models.Proxy)\
        .where(models.Proxy.expire > request.expire)
    proxies = await session.execute(query)
    proxies = proxies.all()
    proxy_schema = [schema.proxy.ProxyGetResponse.from_orm(proxy.Proxy) for proxy in proxies]
    if request.type == 'string':
        return [proxy.string_val() for proxy in proxy_schema]
    elif request.type == 'dict[str,str]':
        return [proxy.dict_str_str() for proxy in proxy_schema]
    else: # request.type == 'playwright'
        return [proxy.dict_playwright() for proxy in proxy_schema]


def add_item_to_db(item: schema.proxy.ProxyPost, db: Session):
    db_item = models.Proxy(**item.dict())
    print(item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item