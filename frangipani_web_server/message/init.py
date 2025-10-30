from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.message.base import BaseMessage


@dataclass_json
@dataclass(kw_only=True)
class InitMessage(BaseMessage):
    client_id: str
    root_control_definition: BaseWebControlDefinition
