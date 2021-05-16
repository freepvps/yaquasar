import typing
import dataclasses as dc
from .common import CapabilityBase


@dc.dataclass
class Parameters:
    split: bool


@dc.dataclass
class State:
    instance: str = 'on'
    value: bool = False


@dc.dataclass
class Capability(CapabilityBase):
    TYPE = 'devices.capabilities.on_off'
    PARAMETERS = Parameters
    STATE = State

    type: str = TYPE
    parameters: typing.Optional[Parameters] = None
    state: typing.Optional[State] = None
