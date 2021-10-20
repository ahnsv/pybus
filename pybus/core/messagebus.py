from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

from pybus.core.message import BaseMessage


class MessageBus(ABC):
    @abstractmethod
    def add_handler(self, message: BaseMessage, message_handler: t.Callable):
        pass

    @abstractmethod
    def subscribe(self, message: BaseMessage):
        pass

    @abstractmethod
    def handle(self, message: BaseMessage):
        pass


class MessageBusMiddleware(ABC):
    _next_middleware: MessageBusMiddleware

    def set_next(self, middleware) -> t.Type[MessageBusMiddleware]:
        self._next_middleware = middleware
        return middleware

    @property
    def next_middleware(self) -> MessageBusMiddleware:
        return self._next_middleware

    @abstractmethod
    def handle(self, message) -> BaseMessage:
        if self._next_middleware:
            return self._next_middleware.handle(message)
        return None


class MessageBusMiddlewareChain:
    def __init__(self, middlewares: t.List[MessageBusMiddleware]) -> None:
        self.middlewares = middlewares

    def apply(self):
        middleware_iter = iter(self.middlewares)
        while True:
            try:
                middleware = next(middleware_iter)
                next_middleware = next(middleware_iter)
                middleware.set_next(next_middleware)
            except StopIteration:
                break

    def handle(self, message: BaseMessage) -> ...:
        if not self.middlewares:
            return

        return self.middlewares[0].handle(message)
