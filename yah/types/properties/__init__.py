import typing
from . import floating
from .common import PropertyBase, cast_property


ALL_PROPERTIES: typing.Tuple[typing.Type[PropertyBase], ...]  = (
    floating.Property,
)
PROPERTIES_DICT = {
    item.TYPE: item
    for item in ALL_PROPERTIES
}


__all__ = (
    'on_off',
    'PropertyBase',
    'cast_property',

    'ALL_PROPERTIES',
    'PROPERTIES_DICT',
)
