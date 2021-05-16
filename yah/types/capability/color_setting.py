import enum
import typing
import dataclasses as dc
from .common import CapabilityBase


@dc.dataclass
class TemperatureK:
    min: int
    max: int


@dc.dataclass
class Scene:
    id: str


@dc.dataclass
class ColorScene:
    scenes: typing.List[Scene] = dc.field(default_factory=list)


class ColorMode(enum.Enum):
    hsv: str
    rgb: str


@dc.dataclass
class Parameters:
    color_model: typing.Optional[ColorMode] = None
    temperature_k: typing.Optional[TemperatureK] = None
    color_scene: typing.Optional[ColorScene] = None


@dc.dataclass
class HSV:
    h: int
    s: int
    v: int


@dc.dataclass
class State:
    instance: str
    value: typing.Union[int, str, HSV]

    @classmethod
    def rgb_raw(cls, value: int) -> 'State':
        return cls(instance='rgb', value=value)

    @classmethod
    def rgb(cls, red: int, green: int, blue: int) -> 'State':
        # TODO: check formula
        return cls.rgb_raw(red * 65536 + green * 256 + blue)

    @classmethod
    def temperature_k(cls, value: int) -> 'State':
        return cls(instance='temperature_k', value=value)

    @classmethod
    def hsv(cls, hsv: HSV) -> 'State':
        return cls(instance='hsv', value=hsv)

    @classmethod
    def scene(cls, scene: str) -> 'State':
        return cls(instance='scene', value=scene)


@dc.dataclass
class Capability(CapabilityBase):
    TYPE = 'devices.capabilities.color_setting'
    PARAMETERS = Parameters
    STATE = State

    type: str = TYPE
    parameters: typing.Optional[Parameters] = None
    state: typing.Optional[State] = None
