from big_thing_py.utils.api_util import *
from big_thing_py.utils.exception_util import *
import colorsys


class HejHomeAction(Enum):
    ON = 'on'
    OFF = 'off'
    ZBSW_ON = 'zbsw_on'
    ZBSW_OFF = 'zbsw_off'
    ZBSW_CONTROL = 'zbsw_control'
    CURTAIN_OPEN = 'curtain_onen'
    CURTAIN_CLOSE = 'curtain_close'
    CURTAIN_CONTROL = 'curtain_control'
    BRIGHTNESS = 'brightness'
    COLOR = 'color'
    STATUS = 'status'


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    return colorsys.rgb_to_hsv(r, g, b)


def verify_hejhome_request_result(result_list: list):
    if type(result_list) == list and 'error' in result_list[0]:
        print_error(result_list[0]['error']['description'])
        return False
    else:
        return True
