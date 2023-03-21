from loguru import logger
from fastapi import FastAPI
import routers
import schema


app = FastAPI()

app.include_router(routers.proxy.router)

@app.get('/')
async def home():
    return 'home page'