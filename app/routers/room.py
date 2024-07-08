from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import room as db_room
from app.db import room_user as db_room_user
from app.schemas.room import RoomCreate, RoomCreateResponse, Room, RoomTypes
from app.schemas.room_user import RoomJoined
from typing_extensions import Annotated
from .auth import authenticate_user_token, oauth2_scheme
from app.auth.auth_handler import decode_jwt
from app.models.user import User
from enum import Enum
from app.schemas.response import Response
from fastapi import Query

router = APIRouter(prefix="/rooms", tags=["Rooms"])


class RoomType(str, Enum):
    joined = "joined"
    available = "available"
    created = "created"


@router.get("", status_code=200)
async def get_rooms(current_user: Annotated[User, Depends(authenticate_user_token)], db: Session = Depends(get_db), type: RoomType = Query(None, description="Filter rooms by type."), skip: int = 0, limit: int = 100):
    available_rooms_orm, joined_rooms_orm, created_rooms_orm = [], [], []
    if type == None:
        available_rooms_orm = db_room.get_available_rooms(db)
        joined_rooms_orm = db_room_user.get_joined_rooms_for_user(
            db, current_user.id)
        created_rooms_orm = db_room.get_user_created_rooms(db, current_user.id)
    elif type == RoomType.joined:
        joined_rooms_orm = db_room_user.get_joined_rooms_for_user(
            db, current_user.id)
    elif type == RoomType.available:
        available_rooms_orm = db_room.get_available_rooms(db)
    elif type == RoomType.created:
        created_rooms_orm = db_room.get_user_created_rooms(db, current_user.id)

    joined_rooms_schema = [Room.model_validate(
        room) for room in joined_rooms_orm]
    available_rooms_schema = [Room.model_validate(
        room) for room in available_rooms_orm]
    created_rooms_schema = [Room.model_validate(
        room) for room in created_rooms_orm]

    return Response[RoomTypes](message="Successfully retrieved rooms.", data=RoomTypes(
        joined=joined_rooms_schema,
        available=available_rooms_schema,
        created=created_rooms_schema
    ))


@router.post("", status_code=201)
def create_room(room: RoomCreate, current_user: Annotated[User, Depends(authenticate_user_token)], db: Session = Depends(get_db)):
    _room = db_room.get_room(db, room.name)
    if _room is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room name already exists. Please use a different name.",
        )
    # create room in room table
    created_room = db_room.create_room(db, room, current_user.id)
    # add room and user in room user table
    _created_room_user = db_room_user.join_room(
        db, created_room.id, current_user.id)

    # We'll keep model_validate because we should validate what database is returning to us
    create_room_pydantic_response = RoomCreateResponse.model_validate(
        created_room)
    response = Response[RoomCreateResponse](
        message="Room created succesfully.", data=create_room_pydantic_response)
    return response


@router.post("/{room_id}/join", status_code=200)
def join_room(room_id: int, current_user: Annotated[User, Depends(authenticate_user_token)], db: Session = Depends(get_db)):
    room = db_room.get_room_by_id(db, room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )
    # check if room is joined
    joined_room_user = db_room_user.get_joined_room_for_user(
        db, current_user.id, room.id)
    if joined_room_user is not None:
        return Response[None](
            message="Room already joined.", data=None)
    # join room
    joined_room = db_room_user.join_room(db, room_id, current_user.id)
    joined_room_response_schema = RoomJoined.model_validate(joined_room)
    response = Response[RoomJoined](
        message="Room joined succesfully.", data=joined_room_response_schema)
    return response


@router.post("/{room_id}/leave", status_code=200)
def leave_room(room_id: int, current_user: Annotated[User, Depends(authenticate_user_token)], db: Session = Depends(get_db)):
    room = db_room.get_room_by_id(db, room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found.",
        )
    deleted_count = db_room_user.leave_room(db, room_id, current_user.id)
    if deleted_count == 0:
        return Response[None](
            message="Room already left.", data=None)
    return Response[None](
        message="Room left.", data=None)
