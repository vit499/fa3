from fastapi import Depends, APIRouter
import logging
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db, TimedRoute

logger = logging.getLogger(__name__)

router = APIRouter(route_class=TimedRoute)

@router.get("/", response_model=list[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("def read_rooms")
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    logger.info(f"rooms={len(rooms)}")
    return rooms
