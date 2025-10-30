from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control import ControlOrientationEnum
from frangipani_web_server.control.base.base_input import BaseInputControl


@dataclass_json
@dataclass(kw_only=True)
class Radio(BaseInputControl):
    address: str
    options: list[str]
    value: int

    orientation: ControlOrientationEnum = ControlOrientationEnum.Horizontal
