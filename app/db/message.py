from sqlalchemy.orm import Session

from app.schemas.message import Message
from app.models.message import Message as MessageDB


def get_messages_per_room_id(db: Session, room_id: int, skip: int = 0, limit: int = 10000):
    # Add more filters like time, duration(past 24 hours etc)
    return db.query(MessageDB).filter(MessageDB.room_id == room_id).offset(skip).all()


def add_message(db: Session, room_id: int, message: Message):
    try:
        message_dict = message.model_dump()
        db_msg = MessageDB(uid=str(message_dict['uid']), sender=message_dict['sender'],
                           message=message_dict['message'], sent=message_dict['sent'], room_id=room_id)

        db.add(db_msg)
        db.commit()
        db.refresh(db_msg)
        return db_msg
    except Exception as e:
        print(
            f"Database call: message: add_message: An unexpected error occurred: {e}")
