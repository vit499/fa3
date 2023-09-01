from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from .database import Base
from app.db.base_class import Base


class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    param = Column(String)
    status = Column(String)

    rooms = relationship("Room", back_populates="owner")


