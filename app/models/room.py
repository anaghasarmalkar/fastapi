from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from .base import Base
from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime, default=func.datetime('now', 'utc'))
    created_by = Column(Integer, ForeignKey("user.id"))
    modified = Column(DateTime, default=func.datetime('now', 'utc'))
    modified_by = Column(Integer, ForeignKey("user.id"))

    users = relationship('RoomUser', back_populates='room')
