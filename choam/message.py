from enum import Enum
from typing import Optional

from rich.console import Console

from choam.constants import OPERATING_SYSTEM

console = Console()


class MessageType(Enum):
    NORMAL = "NORMAL"
    GOOD = "GOOD"
    WARNING = "WARNING"
    ERROR = "ERROR"


message_styles = {
    MessageType.NORMAL.name: "white",
    MessageType.GOOD.name: "white on green",
    MessageType.WARNING.name: "yellow",
    MessageType.ERROR.name: "white on red",
}


class Message:
    """
    Console message using Rich with styling abilities
    and proper Choam formatting
    """

    types = MessageType

    def __init__(self, content: str, _type: Optional[Enum] = None):
        self.content = content

        self._type = _type
        if not self._type:
            self._type = self.types.NORMAL

    def send(self):
        """
        Sends the message to the console
        """

        console.print(f"\t[{self.style}] {self.content} [/{self.style}]\n")

    @property
    def style(self):
        return message_styles.get(self.type.name, self.types.NORMAL.name)

    @property
    def type(self):
        return self._type


class MessageArray:
    """
    A class defining a group of messages
    """

    def __init__(
        self, content: "list[str]", _type: Optional[Enum] = Message.types.NORMAL
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


class Messenger:
    types = Message.types

    def __init__(self):
        self._history = []

    def log(self, content: str, _type: Optional[MessageType] = None):
        self.newline()
        message = Message(content, _type)
        message.send()

        self._history.append(message)

    def log_single_line(self, content: str, _type: Optional[MessageType] = None):
        message = Message(content, _type)

        console.print(f"\t[{message.style}]{message.content}[/{message.style}]")

        self._history.append(message)

    def log_array(self, content: "list[str]"):
        MessageArray(content).send()

    def newline(self):
        """
        Print a new line to the console
        """
        print()

    def session(self):
        return MessengerSession()

    @property
    def history(self):
        return self._history


class MessengerSessionLogger(Messenger):
    """
    Typical messenger logging meant for
    specific sessions
    """

    # trunk-ignore(pylint/W0235)
    def __init__(self) -> None:
        super().__init__()

    def log(self, content: str, _type: Optional[MessageType] = None):
        self.log_single_line(content, _type)


class MessengerSession:
    def __init__(self) -> None:
        self._active_messenger = None

    def __enter__(self):
        print()
        return MessengerSessionLogger()

    def __exit__(self, _type, _value, _traceback):
        if OPERATING_SYSTEM != "windows":
            print()


if __name__ == "__main__":
    messenger = Messenger()

    # Used for logging tasks as they happen
    with messenger.session() as session:
        session.log("Hello, world!")
        session.log("Attempting additional section")
        session.log(
            "(ignored) Fatal: Application can't properly run without proper configurations",
            _type=session.types.ERROR,
        )
