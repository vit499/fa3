from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import update

from app import models, schemas
import logging

logger = logging.getLogger(__name__)

def get_flat(db: Session, flat_id: int):
    a = db.query(models.Flat).filter(models.Flat.id == flat_id).first()
    return a


def get_flat_by_name(db: Session, name: str):
    a = db.query(models.Flat).filter(models.Flat.name == name).first()
    return a

def get_flat_id_by_name(db: Session, name: str):
    id = db.query(models.Flat).filter(models.Flat.name == name).first().id
    return id

def get_flats(db: Session, skip: int = 0, limit: int = 100):
    logger.info("crud get_flats")
    a = db.query(models.Flat).offset(skip).limit(limit).all()
    logger.info(f"a={len(a)}")
    return a 


def create_flat(db: Session, flat: schemas.FlatCreate):
    db_flat = models.Flat(**flat.dict())
    db.add(db_flat)
    db.commit()
    db.refresh(db_flat)
    return db_flat

def update_flat(db: Session, flat_id: int, flat_status: str):
    # print(f"flat_to_update={flat_to_update.name},{flat_to_update.status}")
    # flat_old = db.query(models.Flat).filter(models.Flat.id == flat_id).first()
    # if flat_old.status == flat_status:
    #     logger.info(f"flat not changed")
    #     return flat_old
    
    stmt = (
        update(models.Flat).
        where(models.Flat.id == flat_id).
        values({'status': flat_status})
    )
    # print(f"stmt={stmt}")
    db.execute(stmt)
    db.commit()
    flat = db.query(models.Flat).filter(models.Flat.id == flat_id).first()
    return flat

def del_flats(db: Session):
    logger.info("crud flats del")
    db.execute(text('DELETE FROM dots'))
    db.commit()
    db.execute(text('DELETE FROM rooms'))
    db.commit()
    db.execute(text('DELETE FROM flats'))
    db.commit()
    a = db.query(models.Flat).all()
    logger.info(f"a={len(a)}")
    return a 
