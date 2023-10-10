#!/bin/python


from big_thing_py.big_thing import *
from timelapse_utils import *

import argparse


timelapse = TimelapseCamera()


def timelapse_start() -> bool:
    timelapse.start_capture()
    return True


def timelapse_stop() -> bool:
    timelapse.stop_capture()
    return True


def make_video(dst_path: str) -> bool:
    result = timelapse.make_video(dst_path=dst_path)
    return result


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='timelapse_big_thing', help="thing name"
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
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    timelapse.run_thread()
    tag_list = [MXTag(name='timelapse')]

    value_list = []
    function_list = [
        MXFunction(
            func=timelapse_start,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=timelapse_stop,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=make_video,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='video_dst_path',
                    bound=(0, 1000),
                    type=MXType.STRING,
                )
            ],
        ),
    ]

    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        service_list=function_list + value_list,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
