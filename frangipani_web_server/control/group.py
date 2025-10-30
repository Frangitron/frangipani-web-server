from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base.base import BaseControl


@dataclass_json
@dataclass(kw_only=True)
class Group(BaseControl):
    controls: list[BaseControl]
