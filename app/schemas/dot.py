from typing import Union

from pydantic import BaseModel

# flat1 -> room1 -> dot1
#                -> dot2
#          room2 -> dot3
#                -> dot4
#          room3 -> dot5
# flat2 -> room4 -> dot6

class DotBase(BaseModel):
    param: Union[str, None] = None
    status: Union[str, None] = None


class DotCreate(DotBase):
    pass


class Dot(DotBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


