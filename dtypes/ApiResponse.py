from .HttpStatus import HttpStatus
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    status: HttpStatus
    message: str
    data: T

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data
        }
