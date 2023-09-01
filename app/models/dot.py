from ast import Param
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from .database import Base
from app.db.base_class import Base


class Dot(Base):
    __tablename__ = "dots"

    id = Column(Integer, primary_key=True, index=True)
    param = Column(String)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("rooms.id"))

    owner = relationship("Room", back_populates="dots")

