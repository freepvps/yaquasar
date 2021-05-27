import typing
import dataclasses as dc
from ..common import Unixtime
from ..._base import as_dict, from_dict


Parameters = typing.Any
State = typing.Any


@dc.dataclass
class CapabilityBase:
    TYPE = ''
    PARAMETERS = Parameters
    STATE = State

    type: str = TYPE
    reportable: typing.Optional[bool] = None
    retrievable: typing.Optional[bool] = None
    last_updated: typing.Optional[Unixtime] = None
    parameters: typing.Optional[Parameters] = None
    state: typing.Optional[State] = None

    def validate_as_parameters(self) -> None:
        if self.reportable is None or self.retrievable is None or self.parameters is None:
            raise ValueError('invalid state for parameters')

    def valiadate_as_state(self) -> None:
        if self.state is None:
            raise ValueError('invalid state for parameters')


C = typing.TypeVar('C', bound=CapabilityBase)


def cast_capability(value: CapabilityBase, target_type: typing.Type[C]) -> C:
    parameters_type: typing.Type[typing.Any] = target_type.PARAMETERS
    state_type: typing.Type[typing.Any] = target_type.STATE
    return target_type(
        type=value.type,
        reportable=value.reportable,
        retrievable=value.retrievable,
        last_updated=value.last_updated,
        parameters=from_dict(parameters_type, as_dict(value.parameters)),
        state=from_dict(state_type, as_dict(value.state)),
    )
