import typing
import dataclasses as dc
from .common import PropertyBase


@dc.dataclass
class Parameters:
    instance: str
    name: typing.Optional[str]
    unit: typing.Optional[str]


@dc.dataclass
class State:
    value: float = 0.0


@dc.dataclass
class Property(PropertyBase):
    TYPE = 'devices.properties.float'
    PARAMETERS = Parameters
    STATE = State

    type: str = TYPE
    parameters: typing.Optional[Parameters] = None
    state: typing.Optional[State] = None
