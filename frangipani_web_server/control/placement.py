from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Placement:
    column: int
    row: int
    spanColumn: int = 1
    spanRow: int = 1
