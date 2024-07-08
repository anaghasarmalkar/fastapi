from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Union, List
from datetime import datetime


class RoomBase(BaseModel):
    name: str
    description: Union[str, None]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Test Room",
                "description": "Test Description"
            }
        }
        from_attributes = True


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    created: datetime
    created_by: int

    model_config = ConfigDict(from_attributes=True)


class RoomTypes(BaseModel):
    joined: List[Room]
    available: List[Room]
    created: List[Room]

    model_config = ConfigDict(from_attributes=True)


class RoomCreateResponse(RoomBase):
    id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)
