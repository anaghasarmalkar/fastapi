from fastapi import APIRouter
from app.routers.ws.room import room

router = APIRouter(prefix="/ws", tags=["Websocket"])

router.include_router(room.router)
