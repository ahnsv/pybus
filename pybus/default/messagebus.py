import typing as t
from collections import defaultdict

from pybus.core.message import BaseMessage
from pybus.core.messagebus import MessageBus, MessageBusMiddlewareChain


class DefaultMessageBus(MessageBus):
    def __init__(self, middleware_chain: MessageBusMiddlewareChain = None) -> None:
        self._handlers: t.Dict[BaseMessage, t.List[t.Callable]] = defaultdict(list)
        self._middleware_chain = middleware_chain

    def add_handler(self, message: BaseMessage, message_handler: t.Callable) -> None:
        self._handlers[message].append(message_handler)

    def subscribe(self, message: BaseMessage):
        def message_handler_wrapper(message_handler: t.Callable):
            if not callable(message_handler):
                return

            def wrap_message_handler(*args, **kwargs):
                self._handlers[message].append(message_handler)
                return message_handler

            return wrap_message_handler()

        return message_handler_wrapper

    def handle(self, message: BaseMessage) -> t.List[t.Any]:
        results = []
        if self._middleware_chain:
            message = self._middleware_chain.handle(message=message)
        for handler in self._handlers[type(message)]:
            result = handler(
                message
            )  # TODO(humphrey): check if event handler or command handler
            if result:
                results.append(result)
        return results
