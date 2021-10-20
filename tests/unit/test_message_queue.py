import logging
import queue

import pytest
from _pytest.logging import LogCaptureFixture

from pybus.core.message import Command
from pybus.core.messagebus import MessageBus
from pybus.default.messagebus import DefaultMessageBus

q = queue.Queue()


class FakeCommand(Command):
    name: str


@pytest.fixture
def fake_message_queue():
    return q


@pytest.fixture
def fake_message_bus():
    message_bus = DefaultMessageBus()

    def handle_fake_command(cmd: FakeCommand):
        logging.info(f"{cmd.name}")
        return cmd.name

    message_bus.add_handler(FakeCommand, handle_fake_command)
    return message_bus


@pytest.fixture
def fake_multithreaded_workers(
    fake_message_queue: queue.Queue,
    fake_message_bus: MessageBus,
    num_of_workers=3,
):
    from concurrent.futures import as_completed
    from concurrent.futures.thread import ThreadPoolExecutor

    def process():
        results = []
        while True:
            try:
                message = fake_message_queue.get(block=True, timeout=3.0)
                result = fake_message_bus.handle(message)
                if result:
                    results.append(result)
            except:
                break
        return results

    executor = ThreadPoolExecutor(max_workers=num_of_workers)
    return [executor.submit(process) for _ in range(num_of_workers)]


def test_message_queue_with_workers(
    fake_multithreaded_workers, caplog: LogCaptureFixture
):
    from concurrent.futures import as_completed

    q.put_nowait(FakeCommand(name="hello"))
    q.put_nowait(FakeCommand(name="world"))

    results = [
        future.result()[0]
        for future in as_completed(fake_multithreaded_workers)
        if future.result()
    ]
    print(results)


@pytest.mark.skip
def test_message_queue_without_multithreading(fake_message_bus, benchmark):
    def consume():
        q = queue.Queue()

        for _ in range(100):
            q.put_nowait(FakeCommand(name="hello"))

        results = []
        while True:
            try:
                message = q.get(block=True, timeout=3.0)
                [result] = fake_message_bus.handle(message)
                if result:
                    results.append(result)
            except:
                break

        assert results == ["hello" for _ in range(100)]

    result = benchmark(consume)


def test_message_queue_with_multithreading(fake_message_bus):
    import itertools
    from concurrent.futures import as_completed
    from concurrent.futures.thread import ThreadPoolExecutor

    def consume(_q):
        results = []
        while True:
            try:
                message = _q.get(block=True, timeout=3.0)
                [result] = fake_message_bus.handle(message)
                if result:
                    results.append(result)
            except Exception as exc:
                print(exc)
                break
        return results

    q = queue.Queue()

    for _ in range(100):
        q.put_nowait(FakeCommand(name="hello"))

    executor = ThreadPoolExecutor(max_workers=3)
    futures = [executor.submit(consume, q) for _ in range(3)]
    results = [future.result() for future in as_completed(futures)]
    results = list(itertools.chain(*results))
    assert results == ["hello" for _ in range(100)]
