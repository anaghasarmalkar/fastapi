from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from app.db.database import Base


class RoomUser(Base):
    __tablename__ = "room_user"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_admin = Column(Boolean, default=False)
