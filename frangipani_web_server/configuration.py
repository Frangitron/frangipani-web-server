import dataclasses

from frangipani_web_server.control.base import BaseWebControlDefinition


@dataclasses.dataclass
class WebServerConfiguration:
    control_definitions: list[BaseWebControlDefinition]
    public_folder: str
