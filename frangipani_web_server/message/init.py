from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config

from pythonhelpers.dataclass_json_inheritance_codec import DataclassJsonInheritanceCodec

from frangipani_web_server.control.base.base import BaseControl
from frangipani_web_server.message.base import BaseMessage

_BaseControlCodec = DataclassJsonInheritanceCodec[BaseControl]


@dataclass_json
@dataclass(kw_only=True)
class InitMessage(BaseMessage):
    client_id: str
    root_control_definition: BaseControl = field(
        metadata=config(
            decoder=lambda control: _BaseControlCodec.decode(control, BaseControl),
            encoder=_BaseControlCodec.encode
        )
    )
