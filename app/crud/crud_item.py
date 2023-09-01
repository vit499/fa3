from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app import models, schemas
import logging

logger = logging.getLogger(__name__)


def get_items(db: Session, skip: int = 0, limit: int = 100):
    logger.info("def get_items")
    a = db.query(models.Item).offset(skip).limit(limit).all()
    logger.info(f"a={len(a)}")
    return a # db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def del_items(db: Session):
    logger.info("crud items del_items")
    # db.execute(text('''TRUNCATE TABLE items''').execution_options(autocommit=True))
    # db.execute(text('''TRUNCATE TABLE users CASCADE''').execution_options(autocommit=True))
    # db.execute(text('''TRUNCATE TABLE users CASCADE'''))
    # db.commit()
    db.execute(text('DELETE FROM items'))
    db.commit()
    db.execute(text('DELETE FROM users'))
    db.commit()
    a = db.query(models.Item).all()
    logger.info(f"a={len(a)}")
    return a 
