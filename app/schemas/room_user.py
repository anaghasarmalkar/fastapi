from pydantic import BaseModel, ConfigDict


class RoomJoined(BaseModel):
    room_id: int

    model_config = ConfigDict(from_attributes=True)
