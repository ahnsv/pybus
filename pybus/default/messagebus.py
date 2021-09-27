import typing as t
from collections import defaultdict

from pybus.core.message import Message
from pybus.core.messagebus import MessageBus


class DefaultMessageBus(MessageBus):
    def __init__(self) -> None:
        self._handlers: t.Dict[Message, t.List[t.Callable]] = defaultdict(list)

    def add_handler(self, message: Message, message_handler: t.Callable) -> None:
        self._handlers[message].append(message_handler)

    def subscribe(self, message: Message):
        def message_handler_wrapper(message_handler: t.Callable):
            if not callable(message_handler):
                return

            def wrap_message_handler(*args, **kwargs):
                self._handlers[message].append(message_handler)
                return message_handler

            return wrap_message_handler()

        return message_handler_wrapper

    def handle(self, message: Message) -> t.List[t.Any]:
        results = []
        for handler in self._handlers[type(message)]:
            result = handler(
                message
            )  # TODO(humphrey): check if event handler or command handler
            if result:
                results.append(result)
        if not results:
            return
        return results
