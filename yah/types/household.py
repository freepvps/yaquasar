import typing

import dataclasses as dc
from .room import Room


@dc.dataclass
class Household:
    id: str
    name: str
    is_current: bool
    rooms: typing.List[Room] = dc.field(default_factory=list)
    groups: typing.List[typing.Any] = dc.field(default_factory=list)
    unconfigured_devices: typing.List[typing.Any] = dc.field(default_factory=list)
    speakers: typing.List[typing.Any] = dc.field(default_factory=list)