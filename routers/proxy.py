from fastapi import APIRouter, Query, Depends, HTTPException, Body, Path
from sqlalchemy import insert, select
from config import config
from database import get_async_session, crud, models
from sqlalchemy.orm import Session
from sqlalchemy.engine.result import ChunkedIteratorResult
import schema


router = APIRouter(
    prefix='/proxy',
    tags=['proxy']
)


@router.get('')
async def get_proxy(request: schema.proxy.ProxyGet = Depends(),
                    session: Session = Depends(get_async_session)):
    if request.token != config.token:
        return HTTPException(status_code=401, detail="your token - is bullshit")
    query = select(models.Proxy)
    result = await session.execute(query)
    return result.all()


@router.post('')
async def post_proxy(request: schema.proxy.ProxyPost= Body(), 
                      session: Session = Depends(get_async_session)):
    if request.token != config.token: 
        return HTTPException(status_code=401, detail="your token - is bullshit")
    stmt = insert(models.Proxy).values(request.data.dict())
    return {'status': 'success'}