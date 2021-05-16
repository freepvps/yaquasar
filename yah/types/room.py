import typing
import dataclasses as dc
from .device import Device


@dc.dataclass
class Room:
    id: str
    name: str
    devices: typing.List[Device] = dc.field(default_factory=list)
