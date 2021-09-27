# Pybus 🚌
Type-safe, high-performance message bus for python users powered by pydantic

Use messagebus pattern *without hassel*

## Requirements
- Python >=3.6.2, < 3.9

## Usage
```python
# create messagebus
from pybus.default.messagebus import DefaultMessageBus
messagebus = DefaultMessageBus()

# create messages(commands and events)
from pybus.core.message import Command, Event
from pydantic import Field

class MyCommand(Command):
    name: str

class MyEvent(Event):
    name: str 

# create handlers

def handle_mycommand(cmd: MyCommand):
    return cmd.name

def handle_myevent(event: MyEvent):
    print(event.name)

# add handlers to message bus 
messagebus.add_handler(MyCommand, handle_mycommand)
messagebus.add_handler(MyEvent, handle_myevent)

# handle messages
cmd = MyCommand(name="humphrey")
[result] = messagebus.handle(cmd) # result = "humphrey"

event = MyEvent(name="humphrey")
messagebus.handle(event) # output: "humphrey"


# create handlers with decorator, and skip add handler part
@messagebus.subscribe(MyCommand)
def handle_mycommand(cmd: MyCommand):
    return cmd.name

@messagebus.subscribe(MyEvent)
def handle_myevent(event: MyEvent):
    print(event.name)

cmd = MyCommand(name="humphrey")
[result] = messagebus.handle(cmd) # result = "humphrey"

event = MyEvent(name="humphrey")
messagebus.handle(event) # output: "humphrey"
```