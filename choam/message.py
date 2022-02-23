from enum import Enum
from typing import Optional

from rich.console import Console
console = Console()

class MessageType(Enum):
    NORMAL      = "NORMAL"
    GOOD        = "GOOD"
    WARNING     = "WARNING"
    ERROR       = "ERROR"

message_styles = {
    MessageType.NORMAL.name  : "white",
    MessageType.GOOD.name    : "white on green",
    MessageType.WARNING.name : "yellow",
    MessageType.ERROR.name   : "white on red"
}

class Message:
    '''
    Console message using Rich with styling abilities
    and proper Choam formatting
    '''
    types = MessageType

    def __init__(
        self,
        content: str,
        _type: Optional[Enum] = MessageType.NORMAL
    ):
        self.content = content
        self._type = _type

    def send(self):
        '''
        Sends the message to the console
        '''
        message_style = message_styles[self.type.name]
        
        console.print(f"\t[{message_style}] {self.content} [/{message_style}]\n")

    @property
    def type(self):
        return self._type

class MessageArray:
    '''
    A class defining a group of messages
    '''

    def __init__(
        self,
        content: "list[str]",
        _type: Optional[Enum] = Message.types.NORMAL
    ):
        self.content = content
        self._type = _type

    def add_message(self, message):
        self.content.append(message)

    def send(self):
        message_style = message_styles[self.type.name]

        messages = [Message(message, self._type) for message in self.content]

        print()

        for message in messages:
            console.print(f"\t[{message_style}] {message.content} [/{message_style}]")

        print()

    @property
    def type(self):
        return self._type

if __name__ == "__main__":
    m1 = Message("hello, world!", Message.types.NORMAL)
    m2 = Message("hello, world!", Message.types.GOOD)
    m3 = Message("hello, world!", Message.types.WARNING)
    m4 = Message("hello, world!", Message.types.ERROR)

    m1.send()
    m2.send()
    m3.send()
    m4.send()

    message_array = MessageArray([
        "hello, world",
        "hello, world"
    ])

    message_array.send()

class Messenger:
    def __init__(self):
        pass

    def log(self, content: str, _type: Optional[str] = None):
        message = Message(content, _type)
        message.send()

    def session(self):
        pass