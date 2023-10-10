from big_thing_py.utils.api_util import *
from big_thing_py.utils.exception_util import *


class SmartThingsAction(Enum):
    ON = 'on'
    OFF = 'off'
    BRIGHTNESS = 'brightness'
    COLOR = 'color'
    STATUS = 'status'


# TODO: complete this class implementation


class SmartThingsCommend:
    def __init__(self) -> None:
        self._component = None
        self._capability = None
        self._command = None
        self._arguments = None


def get_device_capabilities(device_info: dict) -> List[str]:
    return device_info['capabilities']
