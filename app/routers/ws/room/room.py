from pydantic import ValidationError
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException
from app.db.database import get_db
from app.routers.api.auth.auth import validate_jwt_token_ws
from sqlalchemy.orm import Session
from app.routers.ws.room.connection_manager import ConnectionManager
from app.schemas.message import IncomingMessage, Message
import json
from app.db import message as message_db
# TODO: Sub routes of room
router = APIRouter(prefix="/rooms", tags=["Room"])

# async def periodic_token_validation(websocket: WebSocket, token: str):
#     while True:
#         await as

# dict of active connections per room
ACTIVE_CONNECTIONS_PER_ROOM = {}

# dict of messages per room
# Store in db, but when to store
MESSAGES_PER_ROOM = {}

# Messages for active connections per room can be stored in redis channel using pubsub

# how will messages get to people who are not connected
# received by can be stored message table as json array. received by is the list of currently active users, very different than members of the room. members of the room will get messages on initial room load. 1) get messages on room open, 2) open socket connection

# n Python, **data is used to unpack a dictionary (data) into keyword arguments in function calls or when creating instances of classes. This syntax is part of Python's capabilities to handle variable-length argument lists and is known as dictionary unpacking.

manager = ConnectionManager()


@router.websocket("/{room_id}/chat")
async def send_message(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    # Open connection
    manager.set_room(room_id)
    await manager.connect(websocket)

    try:
        # get user auth token in the first message only
        data = await websocket.receive_json()
        current_user = await validate_jwt_token_ws(data, db)

        while True:
            data = await websocket.receive_json()
            incoming_message = IncomingMessage(**data)
            message = Message(
                **incoming_message.model_dump(), sender=current_user.id)

            # add to rooms
            manager.add_message(message)
            message_db.add_message(db, room_id, message)
            await manager.broadcast(websocket, message.model_dump_json())

    # handle exceptions when websocket conn is closed (by the client for ex)
    # no WebSocketException because socket is disconnected. cant send anything back.
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)

    except ValidationError as e:
        # control frame is still long if there are more than 1 objects in the array
        val_errors = e.errors(
            include_url=False, include_input=False, include_context=False)
        raise WebSocketException(code=1000, reason=json.dumps(val_errors))

    except WebSocketException as e:
        await websocket.send_text(f"WebSocket error: {e.reason}")
        await websocket.close(code=e.code)
        manager.disconnect(websocket)

    except Exception as e:
        print(
            f"Routers::WS::room::send_message:: An unexpected error occurred: {e}")
