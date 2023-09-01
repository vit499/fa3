
from typing import Generator
import logging
from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute
import time
from typing import Callable

from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

def get_db() -> Generator:
    # logger.info("get_db")
    try:
        db = SessionLocal()
        yield db
    finally:
        # logger.info("db close")
        db.close()

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response = await original_route_handler(request)
            # response: Response = await original_route_handler(request)
            duration = time.time() - before
            # response.headers["X-Response-Time"] = str(duration)
            if duration > 1:
                logger.info(f"req: {duration}")
            # print(f"route response: {response}")
            # print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


