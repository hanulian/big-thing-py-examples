#!/bin/python

import argparse
from datetime import datetime
from big_thing_py.big_thing import *
from camera_utils import camera_capture


def capture() -> str:
    formattedDate = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'{formattedDate}.jpg'
    result = camera_capture(file_name, 0)
    if result:
        return os.path.abspath(file_name)
    else:
        return 'Capture Fail'


def capture_with_filename(file_name: str) -> str:
    result = camera_capture(file_name, 0)
    if result:
        return os.path.abspath(file_name)
    else:
        return 'Capture Fail'


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='camera_big_thing', help="thing name"
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
    tag_list = [
        MXTag(name='camera'),
        MXTag(name='big_thing'),
    ]
    function_list = [
        MXFunction(func=capture, exec_time=10, timeout=10, return_type=MXType.STRING, tag_list=tag_list, arg_list=[]),
        MXFunction(
            func=capture_with_filename,
            exec_time=10,
            timeout=10,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='image_name_arg', type=MXType.STRING, bound=(0, 10000))],
        ),
    ]
    value_list = []

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
