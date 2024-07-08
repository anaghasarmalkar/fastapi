from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base


class RoomUserRole(Base):
    __tablename__ = "room_user_role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class RoomUser(Base):
    __tablename__ = "room_user"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    # user_role_id = Column(Integer, ForeignKey('room_user_role.id'))
    joined = Column(DateTime, default=func.datetime('now', 'utc'))

    room = relationship('Room', back_populates='users')
    user = relationship('User', back_populates='rooms')
    # role = relationship('RoomUserRole')
