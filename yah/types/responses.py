import typing
import dataclasses as dc
from .household import Household


@dc.dataclass
class ResponseBase:
    status: str
    request_id: str


@dc.dataclass
class HouseholdsResponse(ResponseBase):
    households: typing.List[Household] = dc.field(default_factory=list)
