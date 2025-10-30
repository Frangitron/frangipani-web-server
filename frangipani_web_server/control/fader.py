from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base.base_input import BaseInputControl
from frangipani_web_server.control.base.enum_orientation import ControlOrientationEnum


@dataclass_json
@dataclass(kw_only=True)
class Fader(BaseInputControl):
    address: str
    value: float

    orientation: ControlOrientationEnum = ControlOrientationEnum.Horizontal
    max: float | None = None
    min: float | None = None
