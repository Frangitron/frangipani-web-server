from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.placement import Placement


@dataclass_json
@dataclass
class BaseWebControlDefinition:
    label: str
    placement: Placement
