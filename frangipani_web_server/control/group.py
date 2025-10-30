from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.control.definition import WebControlDefinition


@dataclass_json
@dataclass
class WebControlGroupDefinition(BaseWebControlDefinition):
    controls: list[WebControlDefinition]
