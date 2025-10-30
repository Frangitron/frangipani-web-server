from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseMessage:
    """
    BaseMessage serves as a foundation for creating message objects with
    automatic type identification.

    This class is intended to be used as a base class for message models. It
    uses JSON capabilities for serialization and deserialization of data
    fields. Upon initialization, the class automatically assigns the `type`
    attribute using the class name.

    Attributes:
        type: This attribute is dynamically set during initialization and
        stores the class name of the object. The purpose of this field is to
        identify the specific type of message.

    """
    _type: str | None = None  # FIXME find a better than using kw_only=True in subclasses

    def __post_init__(self):
        self._type = self.__class__.__name__
