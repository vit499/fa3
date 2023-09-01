from sqlalchemy.orm import Session
from sqlalchemy import update

from app import models, schemas
import logging

logger = logging.getLogger(__name__)


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    logger.info("def get_rooms")
    a = db.query(models.Room).offset(skip).limit(limit).all()
    logger.info(f"a={len(a)}")
    return a # db.query(models.Item).offset(skip).limit(limit).all()


def create_room(db: Session, room: schemas.RoomCreate, flat_id: int):
    room_old = db.query(models.Room).where(models.Room.owner_id == flat_id).where(models.Room.param == room.param).first()
    if room_old is None:
        db_room = models.Room(**room.dict(), owner_id=flat_id)
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room
    
    # if(room_old.status == room.status):
    #     logger.info(f"room not changed")
    #     return room_old

    stmt = (
        update(models.Room).
        where(models.Room.id == room_old.id).
        values({'status': room.status})
    )
    db.execute(stmt)
    db.commit()
    room = db.query(models.Room).filter(models.Room.id == room_old.id).first()
    return room

def update_room(db: Session, param: str, status: str, flat_id: int):
    # room_old = db.query(models.Room).where(models.Room.owner_id == flat_id).where(models.Room.param == param).first()
    # if(room_old.status == status):
    #     # logger.info(f"room {param} not changed")
    #     return room_old

    stmt = (
        update(models.Room).
        # where(models.Room.id == room_old.id).
        where(models.Room.owner_id == flat_id).
        where(models.Room.param == param).
        values({'status': status})
    )
    db.execute(stmt)
    db.commit()
    room_old = db.query(models.Room).where(models.Room.owner_id == flat_id).where(models.Room.param == param).first()
    return room_old


