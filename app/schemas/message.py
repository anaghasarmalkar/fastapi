from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


class IncomingMessage(BaseModel):
    message: str


# https://docs.pydantic.dev/2.7/concepts/models/#fields-with-dynamic-default-values

def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Message(IncomingMessage):
    sender: int
    sent: datetime = Field(default_factory=datetime_now)
    uid: UUID = Field(default_factory=uuid4)


class AuthMessage(BaseModel):
    access_token: str


class MessageDB(BaseModel):
    uid: str
    room_id: int
    message: str
    sender: int
    sent: datetime

    model_config = ConfigDict(from_attributes=True)
