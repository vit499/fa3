from sqlalchemy.orm import Session
from sqlalchemy import update

from app import models, schemas
import logging

logger = logging.getLogger(__name__)

def save_dot(db: Session, dot: schemas.Dot, room_id: int):
    db_dot = models.Dot(**dot.dict(), owner_id=room_id)
    db.add(db_dot)
    db.commit()
    db.refresh(db_dot)
    return db_dot

def create_dot(db: Session, dot: schemas.DotCreate, room_id: int):
    dot_old = db.query(models.Dot).where(models.Dot.owner_id == room_id).where(models.Dot.param == dot.param).first()
    if dot_old is None:
        db_dot = models.Dot(**dot.dict(), owner_id=room_id)
        db.add(db_dot)
        db.commit()
        db.refresh(db_dot)
        return db_dot
    
    # if(dot_old.status == dot.status):
    #     logger.info(f"dot not changed")
    #     return db_dot

    stmt = (
        update(models.Dot).
        where(models.Dot.id == dot_old.id).
        values({'status': dot.status})
    )
    db.execute(stmt)
    db.commit()
    dot = db.query(models.Dot).filter(models.Dot.id == dot_old.id).first()
    return dot

def update_dot(db: Session, param: str, status: str, room_id: int):
    # dot_old = db.query(models.Dot).where(models.Dot.owner_id == room_id).where(models.Dot.param == param).first()
    # if(dot_old.status == status):
    #     # logger.info(f"dot not changed")
    #     return dot_old

    stmt = (
        update(models.Dot).
        # where(models.Dot.id == dot_old.id).
        where(models.Dot.owner_id == room_id).
        where(models.Dot.param == param).
        values({'status': status})
    )
    db.execute(stmt)
    db.commit()
    # dot_old = db.query(models.Dot).where(models.Dot.owner_id == room_id).where(models.Dot.param == param).first()
    # return dot_old