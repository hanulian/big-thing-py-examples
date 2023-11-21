#!/bin/python

import argparse

from big_thing_py.big_thing import *
from timer_utils import *


timer = Timer()


def is_set() -> float:
    global timer

    return timer.is_set


def start() -> bool:
    global timer

    if timer.timeout is None:
        MXLOG_DEBUG('timer is not set. timeout == None', 'red')
        return False

    return timer.timer_start()


def reset(timeout: float) -> float:
    global timer

    return timer.set_timer(timeout)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='timer_big_thing', help="thing name"
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
        "--append_mac", '-am', action='store_false', required=False, help="append mac address to thing name"
    )
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [MXTag(name='clock')]
    value_list = [MXValue(func=is_set, type=MXType.BOOL, bound=(0, 2), cycle=0.05, tag_list=tag_list)]
    function_list = [
        MXFunction(
            func=start,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=5,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=reset,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=5,
            tag_list=tag_list,
            arg_list=[MXArgument(name='timeout_arg', type=MXType.DOUBLE, bound=(0, 1000000))],
        ),
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


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
