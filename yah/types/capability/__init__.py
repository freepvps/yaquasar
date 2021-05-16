import typing
from . import on_off, color_setting
from .common import CapabilityBase, cast_capability


ALL_CAPABILITIES: typing.Tuple[typing.Type[CapabilityBase], ...] = (
    on_off.Capability,
    color_setting.Capability,
)
CAPABILITIES_DICT = {
    item.TYPE: item
    for item in ALL_CAPABILITIES
}


__all__ = (
    'on_off',
    'color_setting',
    'CapabilityBase',
    'cast_capability',
    'ALL_CAPABILITIES',
    'CAPABILITIES_DICT',
)
