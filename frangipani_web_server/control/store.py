from copy import deepcopy

from frangipani_web_server.control.base import BaseWebControlDefinition
from frangipani_web_server.control.definition import WebControlDefinition
from frangipani_web_server.control.group import WebControlGroupDefinition


class WebControlStore:
    def __init__(self, root_control_definition: BaseWebControlDefinition):
        self._root_control_definition = root_control_definition
        self._updated_controls = {}

        self._make_control_map(self._root_control_definition)

    def get_updated_root_control_definition(self) -> BaseWebControlDefinition:
        return self._get_updated_control_definition(self._root_control_definition)

    def update_control(self, address: str, value: float | bool):
        """
        Updates control value
        """
        # todo assert isinstance ?
        self._updated_controls[address].value = value

    def _make_control_map(self, control: BaseWebControlDefinition):
        if isinstance(control, WebControlDefinition):
            if control.address in self._updated_controls:
                raise ValueError(f"Control address '{control.address}' already exists in map")

            self._updated_controls[control.address] = control

        elif isinstance(control, WebControlGroupDefinition):
            for sub_control in control.controls:
                self._make_control_map(sub_control)

    def _get_updated_control_definition(self, control: BaseWebControlDefinition) -> BaseWebControlDefinition:
        """
        Returns a given control definition, updated with stored value

        Recursively traverses groups
        """
        updated_control = deepcopy(control)

        if isinstance(updated_control, WebControlDefinition):
            updated_control.value = self._updated_controls[control.address].value
            return updated_control

        elif isinstance(updated_control, WebControlGroupDefinition):
            for sub_control in updated_control.controls:
                self._get_updated_control_definition(sub_control)
            return updated_control

        raise RuntimeError(f"Control type '{type(updated_control)}' not supported")
