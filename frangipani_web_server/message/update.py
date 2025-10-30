from dataclasses import dataclass

from dataclasses_json import dataclass_json

from frangipani_web_server.message.base import BaseMessage


@dataclass_json
@dataclass(kw_only=True)
class UpdateMessage(BaseMessage):
    address: str
    sender_id: str
    value: float | bool
