from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.control.enum_orientation import ControlOrientationEnum
from frangipani_web_server.control.enum_type import ControlTypeEnum


@dataclass_json
@dataclass
class WebControlDefinition(BaseWebControlDefinition):
    address: str
    type: ControlTypeEnum
    value: float | bool

    orientation: ControlOrientationEnum = ControlOrientationEnum.Horizontal
    max: float | None = None
    min: float | None = None
