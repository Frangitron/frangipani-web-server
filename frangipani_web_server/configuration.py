import dataclasses
from typing import Callable

from frangipani_web_server.control.base.base import BaseControl
from frangipani_web_server.message.base import BaseMessage


@dataclasses.dataclass
class WebServerConfiguration:
    root_control_definition: BaseControl
    public_folder: str

    message_callback: Callable[[BaseMessage], None] | None = None
