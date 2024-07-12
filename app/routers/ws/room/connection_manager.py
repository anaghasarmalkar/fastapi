from typing import Any, List, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.room_id = None
        self.messages: List[Any] = []
        self.active_connections: Set[WebSocket] = set()

    def set_room(self, room_id: int):
        self.room_id = room_id

    def add_message(self, message: Any):
        self.messages.append(message)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, websocket, message: str):
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_json(message)
