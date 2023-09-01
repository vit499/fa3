import time
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
#from fastapi.logger import logger
import logging

from app.api.api import api_router
from app.core.config import settings

from .dependencies import get_query_token, get_token_header

logger = logging.getLogger(__name__)
logger.info("Initializing app...")


app = FastAPI()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    # logger.info("def root")
    return {"message": "Hello Bigger Applications!"}
