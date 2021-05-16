import dacite
import enum
import typing
import dataclasses as dc


T = typing.TypeVar('T')
DACITE_CONFIG = dacite.Config(  # type: ignore
    check_types=False,
    cast=[enum.Enum, tuple],
)


@dc.dataclass
class _Storage:
    value: typing.Any


def is_dataclass(data: typing.Any) -> bool:
    return dc.is_dataclass(data)


def _normalize_dict(value: typing.Any, drop_nones: bool) -> typing.Any:
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, dict):
        return {
            k: _normalize_dict(v, drop_nones)
            for k, v in value.items()
            if not drop_nones or v is not None
        }
    if isinstance(value, (list, tuple)):
        return [
            _normalize_dict(v, drop_nones)
            for v in value
        ]
    if isinstance(value, (int, float, str, bool)):
        return value
    if value is None:
        return None
    return value


def as_dict(value: T, drop_nones: bool = True) -> typing.Any:
    if dc.is_dataclass(value):
        return _normalize_dict(dc.asdict(value), drop_nones=drop_nones)
    else:
        return as_dict(_Storage(value), drop_nones)['value']


def from_dict(data_type: typing.Type[T], value: typing.Any) -> T:
    result: T
    if dc.is_dataclass(data_type):
        result = dacite.from_dict(  # type: ignore
            data_type,
            value,
            DACITE_CONFIG,
        )
    else:
        basic_type: typing.Type[typing.Any] = dc.make_dataclass('X', [('value', data_type)])
        result = from_dict(basic_type, {'value': value}).value
    return result
