from typing import Union

from pydantic import BaseModel
from .dot import Dot

# flat1 -> room1 -> dot1
#                -> dot2
#          room2 -> dot3
#                -> dot4
#          room3 -> dot5
# flat2 -> room4 -> dot6

class RoomBase(BaseModel):
    param: Union[str, None] = None
    status: Union[str, None] = None


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    owner_id: int
    dots: list[Dot] = []

    class Config:
        from_attributes = True

class RoomX(BaseModel):
    src: Union[str, None] = None


