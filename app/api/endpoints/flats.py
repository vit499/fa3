from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import logging
# from pydantic import BaseModel
from app.core.config import settings

from app import schemas, crud, models
from app.api.deps import get_db, TimedRoute

logger = logging.getLogger(__name__)

router = APIRouter(route_class=TimedRoute)

@router.post("/", response_model=schemas.Flat)
def create_flat(flat: schemas.FlatCreate, db: Session = Depends(get_db)):
    # logger.info("def create_flat")
    # logger.info(f"name={flat.name}")
    # logger.info(f"param={flat.param}")
    # logger.info(f"status={flat.status}")
    db_flat = crud.get_flat_by_name(db, name=flat.name)
    if db_flat:
        # raise HTTPException(status_code=400, detail="Flat already registered")
        r = crud.update_flat(db=db, flat_id=db_flat.id, flat_status=flat.status)
    else:
        raise HTTPException(status_code=400, detail="Flat not found")
        # r = crud.create_flat(db=db, flat=flat)
    # logger.info(f"flat.id={r.id}")
    return r

@router.post("/{flat_name}", response_model=schemas.Flat)
def create_flat(flat_name: str, db: Session = Depends(get_db)):
    # logger.info("def create_flat")
    # logger.info(f"name={flat_name}")
    db_flat = crud.get_flat_by_name(db, name=flat_name)
    if db_flat:
        raise HTTPException(status_code=400, detail="Flat already registered")
        # r = crud.update_flat(db=db, flat_id=db_flat.id, flat_status=db_flat.status)
    else:
        r = create_flat_and_rooms(db=db, name=flat_name)
    # logger.info(f"flat.id={r.id}")
    return r


@router.get("/", response_model=list[schemas.Flat])
def read_flats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flats = crud.get_flats(db, skip=skip, limit=limit)
    return flats


# @router.get("/{flat_id}", response_model=schemas.Flat)
# def read_flat(flat_id: int, db: Session = Depends(get_db)):
#     db_flat = crud.get_flat(db, flat_id=flat_id)
#     if db_flat is None:
#         raise HTTPException(status_code=404, detail="Flat not found")
#     return db_flat

@router.get("/{flat_name}", response_model=schemas.Flat)
def read_flat_by_name(flat_name: str, db: Session = Depends(get_db)):
    db_flat = crud.get_flat_by_name(db, name=flat_name)
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    return db_flat

@router.get("/{flat_name}/r")
def read_flat_by_name(flat_name: str, db: Session = Depends(get_db)):
    db_flat = crud.get_flat_by_name(db, name=flat_name)
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    flat = schemas.Flat.model_validate(db_flat)
    return flat

@router.delete("/", response_model=list[schemas.Flat])
def del_flats(db: Session = Depends(get_db)):
    logger.info("router flats delete")
    flats = crud.del_flats(db)
    logger.info(f"flats={len(flats)}")
    return flats


def create_flat_and_rooms(name: str, db: Session):
    flat = schemas.FlatCreate(
        name=name,
        param="f1",
        status="1"
    )
    f = crud.create_flat(db=db, flat=flat)

    for i in range(0, settings.MAX_ROOM):
        room = schemas.RoomCreate(
            param=f"f{f.name}_r{i+1}",
            status="1"
        )
        r = crud.create_room(db=db, room=room, flat_id=f.id)

        for j in range(0, settings.MAX_DOT):
            dot = schemas.DotCreate(
                param=f"{r.param}_d{j+1}",
                status="1"
            )
            crud.create_dot(db=db, dot=dot, room_id=r.id)
    return f

def update_flat_and_rooms(f: models.Flat, flat_status: str, room_status: list[str], dot_status: list[str], db: Session):
    status = f.status
    if flat_status != status:
        f = crud.update_flat(db=db, flat_id=f.id, flat_status=flat_status)
    for i in range(0, settings.MAX_ROOM):
        r = f.rooms[i]
        status = r.status
        if room_status[i] != status:
            r = crud.update_room(db=db, param=f"f{f.name}_r{i+1}", status=room_status[i], flat_id=f.id)
        for j in range(0, settings.MAX_DOT):
            d = r.dots[j]
            status = d.status
            if dot_status[i*settings.MAX_DOT+j] != status:
                crud.update_dot(db=db, param=f"{r.param}_d{j+1}", status=dot_status[i*settings.MAX_DOT+j], room_id=r.id)
    return f

@router.post("/{flat_name}/xx/", response_model=schemas.Flat)
def update_all(
    flat_name: str, roomX: schemas.RoomX, db: Session = Depends(get_db)
):
    # src=  flat=55&room=4154136146&dot=11
    # logger.info(f"def xx {roomX.src}")
    MAX_ROOM_LEN = settings.MAX_ROOM * 2
    MAX_DOT_LEN = settings.MAX_DOT * 2 * settings.MAX_ROOM
    a = roomX.src.split("&")
    flat_status = a[0].split("=")[1]
    b = a[1].split("=")[1]
    if len(b) < MAX_ROOM_LEN:
        b = b + "0" * (MAX_ROOM_LEN - len(b))
    if len(b) > MAX_ROOM_LEN:
        b = b[:MAX_ROOM_LEN]
    room_status = get_values_from_str(b, settings.MAX_ROOM)
    c = a[2].split("=")[1]
    if len(c) < MAX_DOT_LEN:
        c = c + "0" * (MAX_DOT_LEN - len(c))
    if len(c) > MAX_DOT_LEN:
        c = c[:MAX_DOT_LEN]
    dot_status = get_values_from_str(c, settings.MAX_DOT * settings.MAX_ROOM) 
    
    # logger.info(f"flat_status={flat_status}")
    # logger.info(f"room_status={room_status}")
    # logger.info(f"dot_status={dot_status}")
    db_flat = crud.get_flat_by_name(db, name=flat_name)
    if db_flat is None:
        db_flat = create_flat_and_rooms(db=db, name=flat_name)
    # flat = schemas.Flat.model_validate(db_flat)
    db_flat = update_flat_and_rooms(db_flat, flat_status=flat_status, room_status=room_status, dot_status=dot_status, db=db)
    return db_flat

def get_values_from_str(src: str, n: int) -> list[str]:
    # logger.info(f"b={src}")
    r = []
    for i in range(0, n):
        s = src[i*2: i*2+2]
        r.append(s)
    # logger.info(f"r={r}")
    return r