from loguru import logger
from fastapi import FastAPI
import config
import routers

logger.info(f'Start programm')

app = FastAPI()

app.include_router(routers.proxy.router)

