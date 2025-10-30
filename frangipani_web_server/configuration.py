import dataclasses
from typing import Callable

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.message.base import BaseMessage


@dataclasses.dataclass
class WebServerConfiguration:
    root_control_definition: BaseWebControlDefinition
    public_folder: str

    message_callback: Callable[[BaseMessage], None] | None = None
