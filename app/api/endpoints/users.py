from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import logging

from app import schemas, crud
from app.api.deps import get_db, TimedRoute

logger = logging.getLogger(__name__)

router = APIRouter(route_class=TimedRoute)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("def create_user")
    logger.info(f"email={user.email}")
    logger.info(f"password={user.password}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    r = crud.create_user(db=db, user=user)
    logger.info(f"user.id={r.id}")
    return r


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
