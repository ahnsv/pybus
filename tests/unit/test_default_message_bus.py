from pybus.core.message import Command
from dataclasses import dataclass, field
import pytest
from uuid import UUID, uuid4
from pybus.default.messagebus import DefaultMessageBus


@pytest.fixture
def fake_default_message_bus() -> DefaultMessageBus:
    message_bus = DefaultMessageBus()
    return message_bus


def test_default_message_bus_add_handler(fake_default_message_bus: DefaultMessageBus):
    class FakeCommand(Command):
        name: str

    def handle_fake_command(cmd: Command):
        pass

    fake_default_message_bus.add_handler(FakeCommand, handle_fake_command)

    assert handle_fake_command in fake_default_message_bus._handlers[FakeCommand]


def test_default_message_bus_decorator_should_add_handler(
    fake_default_message_bus: DefaultMessageBus,
):
    class FakeCommand(Command):
        name: str

    @fake_default_message_bus.subscribe(FakeCommand)
    def handle_fake_command(cmd: Command):
        pass

    assert handle_fake_command in fake_default_message_bus._handlers[FakeCommand]


def test_default_message_bus_handle_command_should_return_result(
    fake_default_message_bus: DefaultMessageBus,
):
    class FakeCommand(Command):
        name: str

    @fake_default_message_bus.subscribe(FakeCommand)
    def handle_fake_command(cmd: FakeCommand):
        return cmd.name

    cmd = FakeCommand(name="hello")
    [result] = fake_default_message_bus.handle(cmd)

    assert result is not None


def test_default_message_bus_handler_with_extra_parameter_should_pass(
    fake_default_message_bus: DefaultMessageBus,
):
    class FakeCommand(Command):
        id: str
        name: str

    @dataclass
    class FakeEntity:
        id: UUID = field(default_factory=uuid4)
        name: str = field(default=None)

    class FakeRepository:
        def __init__(self) -> None:
            self.items = []

        def add(self, entity):
            self.items.append(entity)
            return str(entity.id)

    @fake_default_message_bus.subscribe(FakeCommand)
    def handle_fake_command(cmd: FakeCommand, repo: FakeRepository = FakeRepository()):
        entity = FakeEntity(name=cmd.name, id=cmd.id)
        return repo.add(entity)

    [result] = fake_default_message_bus.handle(FakeCommand(name="hello", id="world"))

    assert result == "world"
