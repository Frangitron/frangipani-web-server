from enum import StrEnum


class ControlTypeEnum(StrEnum):
    ButtonPress = "button-press"
    ButtonToggle=  "button-toggle"
    ColorWheel = "colorwheel"
    Fader = "fader"
    Radio = "radio"

    Group = "group"
    Spacer = "spacer"
