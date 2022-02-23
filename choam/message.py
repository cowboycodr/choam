from calendar import c
from enum import Enum

class MessageType(Enum):
    NORMAL      = "NORMAL"
    WARNING     = "WARNING"
    ERROR       = "ERROR"

class Message:
    def __init__(
        self,
        content: str,
        _type: str
    ):
        self._content = content
        self._type = _type.upper().strip()

    @property
    def content(self):
        return self._content

    @property
    def type(self):
        return self._type