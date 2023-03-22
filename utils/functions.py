from fastapi import HTTPException
from loguru import logger
from config import config

def check_token(token):
    if config.token != token:
        logger.info('Кто то с плохим токеном')
        raise HTTPException(status_code=401, detail="your token is bullshit")
    