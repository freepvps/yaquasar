import typing
import dataclasses as dc


from .capability import CapabilityBase
from .properties import PropertyBase


@dc.dataclass
class Device:
    id: str
    name: str
    type: str
    icon_url: str = ''
    capabilities: typing.List[CapabilityBase] = dc.field(default_factory=list)
    properties: typing.List[PropertyBase] = dc.field(default_factory=list)
    skill_id: str = ''
    groups: typing.List[typing.Any] = dc.field(default_factory=list)
