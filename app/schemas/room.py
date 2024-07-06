from pydantic import BaseModel, Field, EmailStr
from typing import Union
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
    is_deleted: bool
    created: datetime
    created_by: int
    modified: datetime
    modified_by: int
