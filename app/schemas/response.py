from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

DataT = TypeVar('DataT')


class Response(BaseModel, Generic[DataT]):
    message: str
    data: Optional[DataT] = None
