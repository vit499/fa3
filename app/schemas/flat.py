from typing import Union
from typing import List

from pydantic import BaseModel
from .room import Room

# flat1 -> room1 -> dot1
#                -> dot2
#          room2 -> dot3
#                -> dot4
#          room3 -> dot5
# flat2 -> room4 -> dot6

class FlatBase(BaseModel):
    name: str


class FlatCreate(FlatBase):
    param: Union[str, None] = None
    status: Union[str, None] = None


class Flat(FlatBase):
    id: int
    param: Union[str, None] = None
    status: Union[str, None] = None
    rooms: List[Room] = []

    class Config:
        from_attributes = True


