from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.control.definition import WebControlDefinition
from frangipani_web_server.control.enum_type import ControlTypeEnum


@dataclass_json
@dataclass
class WebControlGroupDefinition(BaseWebControlDefinition):
    controls: list[WebControlDefinition]
    type: ControlTypeEnum = field(default=ControlTypeEnum.Group)
