from big_thing_py.big_thing import *

import time
import random
import argparse


def add_face() -> int:
    return_value = random.randint(0, 100)
    MXLOG_DEBUG(f'{get_current_function_name()} run... return: {return_value}')
    return return_value


def delete_face(int_arg: int) -> int:
    return_value = int_arg
    MXLOG_DEBUG(f'{get_current_function_name()} run... return: {return_value}')
    return return_value


def func_with_arg_and_delay(int_arg: int, deley: float) -> int:
    return_value = int_arg
    MXLOG_DEBUG(f'{get_current_function_name()} run... return: {return_value}')
    MXLOG_DEBUG(f'deley : {deley}')
    time.sleep(deley)
    return return_value


def value_current_time() -> int:
    return_value = int(get_current_time())
    MXLOG_DEBUG(f'{get_current_function_name()} run! return: {return_value}')
    return return_value


def generate_thing(args):
    tag_list = [MXTag(name='basic'), MXTag(name='big_thing')]
    arg_list = [MXArgument(name='int_arg', type=MXType.INTEGER, bound=(0, 10000))]
    delay_arg = MXArgument(name='delay_arg', type=MXType.DOUBLE, bound=(0, 10000))
    function_list = [
        MXFunction(func=func_no_arg, return_type=MXType.INTEGER, tag_list=tag_list, arg_list=[], energy=45),
        MXFunction(func=func_with_arg, return_type=MXType.INTEGER, tag_list=tag_list, arg_list=arg_list, energy=12),
        MXFunction(
            func=func_with_arg_and_delay,
            return_type=MXType.INTEGER,
            timeout=10,
            tag_list=tag_list,
            arg_list=arg_list + [delay_arg],
            energy=56,
        ),
    ]
    value_list = [
        MXValue(func=value_current_time, type=MXType.INTEGER, bound=(0, 2147483647), tag_list=tag_list, cycle=10)
    ]

    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        log_mode=MXPrintMode.get(args.log_mode),
        append_mac_address=args.append_mac,
        service_list=function_list + value_list,
    )
    return thing


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='basic_feature_big_thing', help="thing name"
    )
    parser.add_argument(
        "--host", '-ip', action='store', type=str, required=False, default='127.0.0.1', help="host name"
    )
    parser.add_argument("--port", '-p', action='store', type=int, required=False, default=1883, help="port")
    parser.add_argument(
        "--alive_cycle", '-ac', action='store', type=int, required=False, default=60, help="alive cycle"
    )
    parser.add_argument("--auto_scan", '-as', action='store_true', required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', required=False, help="log enable")
    parser.add_argument(
        "--log_mode", action='store', type=str, required=False, default=MXPrintMode.ABBR.value, help="log mode"
    )
    parser.add_argument(
        "--append_mac",
        '-am',
        action='store_true',  # store_true, store_false
        required=False,
        help="append mac address to thing name",
    )
    args, unknown = parser.parse_known_args()

    return args


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
