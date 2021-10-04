from pybus.core.message import Message
from pybus.core.messagebus import MessageBusMiddleware


def fake_middleware():
    class FakeMiddleware(MessageBusMiddleware):
        def handle(self, message: Message) -> Message:
            print(message)
            return message

    return FakeMiddleware()


def fake_message_bus_with_middleware():
    pass
