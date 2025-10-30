from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.control.base.placement import Placement


@dataclass_json
@dataclass
class BaseControl:
    label: str
    placement: Placement

    _type: str | None = None  # FIXME find a better than using kw_only=True in subclasses

    def __post_init__(self):
        self._type = self.__class__.__name__
