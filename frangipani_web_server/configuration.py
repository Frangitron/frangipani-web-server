from dataclasses import dataclass, field
from typing import Callable

from dataclasses_json import dataclass_json, config
from pythonhelpers.dataclass_json_inheritance_codec import DataclassJsonInheritanceCodec

from frangipani_web_server.control.base.base import BaseControl
from frangipani_web_server.message.base import BaseMessage

_BaseControlCodec = DataclassJsonInheritanceCodec[BaseControl]


@dataclass_json
@dataclass
class WebServerConfiguration:
    root_control_definition: BaseControl = field(
        metadata=config(
            decoder=lambda control: _BaseControlCodec.decode(control, BaseControl),
            encoder=_BaseControlCodec.encode
        )
    )
    public_folder: str

    message_callback: Callable[[BaseMessage], None] | None = None
