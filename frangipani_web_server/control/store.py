from copy import deepcopy

from frangipani_web_server.control.base.base import BaseControl
from frangipani_web_server.control.base.base_input import BaseInputControl
from frangipani_web_server.control.group import Group


class ControlStore:
    def __init__(self, root_control_definition: BaseControl):
        self._root_control_definition = root_control_definition
        self._updated_controls: dict[str, BaseInputControl] = {}

        self._make_control_map(self._root_control_definition)

    def get_updated_root_control(self) -> BaseControl:
        return self._get_updated_control(self._root_control_definition)

    def update_control(self, address: str, value: float | bool):
        """
        Updates control value
        """
        # todo assert isinstance ?
        self._updated_controls[address].value = value

    def _make_control_map(self, control: BaseControl):
        if isinstance(control, Group):
            for sub_control in control.controls:
                self._make_control_map(sub_control)

        elif isinstance(control, BaseInputControl):
            if control.address in self._updated_controls:
                raise ValueError(f"Control address '{control.address}' already exists in map")

            self._updated_controls[control.address] = control

        else:
            raise ValueError(f"Unexpected control type: {type(control)}")

    def _get_updated_control(self, control: BaseControl) -> BaseControl:
        """
        Returns a given control definition, updated with stored value

        Recursively traverses groups
        """
        updated_control = deepcopy(control)

        if isinstance(updated_control, Group):
            for sub_control in updated_control.controls:
                self._get_updated_control(sub_control)
            return updated_control

        elif isinstance(updated_control, BaseInputControl):
            updated_control.value = self._updated_controls[control.address].value
            return updated_control

        raise ValueError(f"Unexpected control type: {type(control)}")
