from big_thing_py.utils.api_util import *
from big_thing_py.utils.exception_util import *
import colorsys


class HejHomeAction(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    ON = auto()
    OFF = auto()
    ZBSW_ON = auto()
    ZBSW_OFF = auto()
    ZBSW_CONTROL = auto()
    CURTAIN_OPEN = auto()
    CURTAIN_CLOSE = auto()
    CURTAIN_CONTROL = auto()
    BRIGHTNESS = auto()
    COLOR = auto()
    STATUS = auto()


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    return colorsys.rgb_to_hsv(r, g, b)


def verify_hejhome_request_result(result_list: list):
    if type(result_list) == list and 'error' in result_list[0]:
        print_error(result_list[0]['error']['description'])
        return False
    else:
        return True
