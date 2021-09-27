from typing import Union

from pydantic import BaseModel


class BaseMessage(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class Command(BaseMessage):
    pass


class Event(BaseMessage):
    pass


Message = Union[Command, Event]
