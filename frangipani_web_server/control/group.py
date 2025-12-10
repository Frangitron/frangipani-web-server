from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config
from pythonhelpers.dataclass_json_inheritance_codec import DataclassJsonInheritanceCodec

from frangipani_web_server.control.base.base import BaseControl


_BaseControlCodec = DataclassJsonInheritanceCodec[BaseControl]


@dataclass_json
@dataclass(kw_only=True)
class Group(BaseControl):
    controls: list[BaseControl] = field(
        metadata=config(
            decoder=lambda controls: [_BaseControlCodec.decode(control, BaseControl) for control in controls],
            encoder=lambda controls_data: [_BaseControlCodec.encode(control_data) for control_data in controls_data]
        )
    )
