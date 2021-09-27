from abc import ABC, abstractmethod
from pybus.core.message import Message
import typing as t


class MessageBus(ABC):
    @abstractmethod
    def add_handler(self, message: Message, message_handler: t.Callable):
        pass

    @abstractmethod
    def subscribe(self, message: Message, message_handler: t.Callable):
        pass

    @abstractmethod
    def handle(self, message: Message):
        pass
