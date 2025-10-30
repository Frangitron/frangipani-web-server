from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base.base import BaseControl


@dataclass_json
@dataclass(kw_only=True)
class Spacer(BaseControl):
    pass
