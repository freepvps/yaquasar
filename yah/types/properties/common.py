import typing
import dataclasses as dc
from ..common import Unixtime
from ..._base import as_dict, from_dict


Parameters = typing.Any
State = typing.Any


@dc.dataclass
class PropertyBase:
    TYPE = ''
    PARAMETERS = Parameters
    STATE = State

    type: str = TYPE
    reportable: typing.Optional[bool] = None
    retrievable: typing.Optional[bool] = None
    parameters: typing.Optional[Parameters] = None
    state: typing.Optional[State] = None

    def validate_as_parameters(self) -> None:
        if self.reportable is None or self.retrievable is None or self.parameters is None:
            raise ValueError('invalid state for parameters')

    def valiadate_as_state(self) -> None:
        if self.state is None:
            raise ValueError('invalid state for state')


C = typing.TypeVar('C', bound=PropertyBase)


def cast_property(value: PropertyBase, target_type: typing.Type[C]) -> C:
    parameters_type: typing.Type[typing.Any] = value.PARAMETERS
    state_type: typing.Type[typing.Any] = value.STATE
    return target_type(
        type=value.type,
        reportable=value.reportable,
        retrievable=value.retrievable,
        parameters=from_dict(parameters_type, as_dict(value.parameters)),
        state=from_dict(state_type, as_dict(value.state)),
    )
