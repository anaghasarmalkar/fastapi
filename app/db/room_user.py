from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.room_user import RoomUser
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import delete


def join_room(db: Session, room_id: int, user_id: int):
    # This is unnecessary. We dont really have a unique or primary key constraint that'll be violated. Nonetheless
    insert_stmt = insert(RoomUser).values(room_id=room_id, user_id=user_id)
    insert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=dict(
            room_id=room_id,
            user_id=user_id,
        )
    )

    # fetch result first before doing commit
    result = db.execute(insert_stmt.returning(RoomUser.room_id)).fetchone()
    db.commit()

    return result


def leave_room(db: Session, room_id: int, user_id: int):
    delete_stmt = delete(RoomUser).where(
        RoomUser.room_id == room_id).where(RoomUser.user_id == user_id)

    result = db.execute(delete_stmt)
    db.commit()

    # Number of rows affected by the delete operation
    return result.rowcount


def get_joined_room_for_user(db: Session, user_id: int, room_id: int):
    return db.query(RoomUser).filter(RoomUser.room_id == room_id, RoomUser.user_id == user_id).first()


def get_joined_rooms_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Room).join(RoomUser).filter(RoomUser.user_id == user_id, Room.is_deleted == False).offset(skip).limit(limit).all()

# def get_joined_users_for_room
