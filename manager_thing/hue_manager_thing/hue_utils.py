from big_thing_py.utils.api_util import *
from big_thing_py.utils.exception_util import *
import math


class MXHueAction(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    IS_ON = auto()
    GET_BRIGHTNESS = auto()
    GET_COLOR = auto()
    GET_DAYLIGHT = auto()
    GET_MOTION = auto()
    GET_LIGHTLEVEL = auto()
    GET_TEMPERATURE = auto()
    ON = auto()
    OFF = auto()
    SET_BRIGHTNESS = auto()
    SET_COLOR = auto()
    STATUS = auto()


class MXHueDeviceType(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    LIGHT = auto()
    SENSOR = auto()


def enhance_color(normalized):
    '''
    Convert RGB to Hue color set
    This is based on original code from http://stackoverflow.com/a/22649803
    '''
    if normalized > 0.04045:
        return math.pow((normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92


# FIXME: implement this function
def rgb_to_xy(r, g, b) -> List[float]:
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = enhance_color(rNorm)
    gFinal = enhance_color(gNorm)
    bFinal = enhance_color(bNorm)

    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0, 0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)

        return [xFinal, yFinal]


def xy_to_rgb(x, y, bri) -> List[float]:
    z = 1.0 - x - y
    Y = bri / 255.0  # Brightness of lamp
    X = (Y / y) * x
    Z = (Y / y) * z
    r = X * 1.612 - Y * 0.203 - Z * 0.302
    g = -X * 0.509 + Y * 1.412 + Z * 0.066
    b = X * 0.026 - Y * 0.072 + Z * 0.962
    r = 12.92 * r if r <= 0.0031308 else (1.0 + 0.055) * pow(r, (1.0 / 2.4)) - 0.055
    g = 12.92 * g if g <= 0.0031308 else (1.0 + 0.055) * pow(g, (1.0 / 2.4)) - 0.055
    b = 12.92 * b if b <= 0.0031308 else (1.0 + 0.055) * pow(b, (1.0 / 2.4)) - 0.055
    maxValue = max(r, g, b)
    r /= maxValue
    g /= maxValue
    b /= maxValue
    r = r * 255
    if r < 0:
        r = 255
    g = g * 255
    if g < 0:
        g = 255
    b = b * 255
    if b < 0:
        b = 255
    return [r, g, b]


def verify_hue_request_result(result_list: list):
    if type(result_list) == list and 'error' in result_list[0]:
        print_error(result_list[0]['error']['description'])
        return False
    else:
        return True


if __name__ == '__main__':
    print(xy_to_rgb(0.4425, 0.406, 254))
