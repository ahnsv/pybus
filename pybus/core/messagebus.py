import typing as t
from abc import ABC, abstractmethod

from pybus.core.message import Message


class MessageBus(ABC):
    @abstractmethod
    def add_handler(self, message: Message, message_handler: t.Callable):
        pass

    @abstractmethod
    def subscribe(self, message: Message):
        pass

    @abstractmethod
    def handle(self, message: Message):
        pass
