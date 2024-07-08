from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate


def get_room_by_id(db: Session, room_id: int):
    # Room returned by the database
    return db.query(Room).filter(Room.id == room_id).first()


def get_room(db: Session, room_name: str):
    # Room returned by the database
    return db.query(Room).filter(Room.name == room_name).first()


def get_available_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).filter(Room.is_deleted == False).offset(skip).limit(limit).all()


def get_created_rooms(db: Session, user_id: int, skip: int = 0, limit: int = 100, ):
    return db.query(Room).filter(Room.created_by == user_id).offset(skip).limit(limit).all()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).filter(Room.is_deleted == False).offset(skip).limit(limit).all()


def get_user_created_rooms(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Room).filter(Room.created_by == user_id, Room.is_deleted == False).offset(skip).limit(limit).all()


def create_room(db: Session, room: RoomCreate, user_id: int):
    # Create a SQLAlchemy model instance with your data.
    db_room = Room(
        name=room.name, description=room.description, created_by=user_id, modified_by=user_id)
    # add that instance object to your database session.
    db.add(db_room)
    # commit the changes to the database (so that they are saved).
    db.commit()
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    db.refresh(db_room)
    return db_room
