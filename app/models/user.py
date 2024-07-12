from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, default=func.datetime('now', 'utc'))

    rooms = relationship('RoomUser', back_populates='user')
    messages = relationship("Message", back_populates="sender_user")
