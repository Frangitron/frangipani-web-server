from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base.placement import Placement


@dataclass_json
@dataclass
class BaseControl:
    label: str
    placement: Placement
