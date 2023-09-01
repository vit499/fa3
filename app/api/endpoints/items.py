from fastapi import Depends, APIRouter
import logging
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db, TimedRoute

logger = logging.getLogger(__name__)

router = APIRouter(route_class=TimedRoute)

@router.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("def read_items")
    items = crud.get_items(db, skip=skip, limit=limit)
    logger.info(f"items={len(items)}")
    return items

@router.get("/delete", response_model=list[schemas.Item])
def del_items(db: Session = Depends(get_db)):
    logger.info("router items delete")
    items = crud.del_items(db)
    logger.info(f"items={len(items)}")
    return items