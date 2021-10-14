import logging

import pytest
from pybus.core.message import Command, Message
from pybus.core.messagebus import MessageBusMiddleware, MessageBusMiddlewareChain
from pybus.default.messagebus import DefaultMessageBus

logger = logging.getLogger(__name__)

@pytest.fixture
def fake_middleware():
    class FakeMiddleware(MessageBusMiddleware):
        def handle(self, message: Message) -> Message:
            logger.info(message)
            return message

    return FakeMiddleware()

class FakeCommand(Command):
    name: str

@pytest.fixture
def fake_message_bus_with_middleware(fake_middleware):
    message_bus_middleware_chain = MessageBusMiddlewareChain(middlewares=[fake_middleware])
    message_bus = DefaultMessageBus(middleware_chain=message_bus_middleware_chain)

    def handle_fake_command(cmd: Command):
        pass

    message_bus.add_handler(FakeCommand, handle_fake_command)
    return message_bus

def test_message_bus_with_logging_middleware(fake_message_bus_with_middleware, caplog):
    cmd = FakeCommand(name="hello")
    with caplog.at_level(logging.DEBUG):
        fake_message_bus_with_middleware.handle(message=cmd)
    assert "hello" in caplog.text

