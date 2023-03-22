from loguru import logger
from fastapi import FastAPI
import routers

app = FastAPI()

app.include_router(routers.proxy.router)

