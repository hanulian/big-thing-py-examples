#!/bin/python

from big_thing_py.big_thing import *

import argparse
from music_player_utils import VLCPlayer

vlc_player = VLCPlayer()


def play(source: str) -> bool:
    global vlc_player

    try:
        vlc_player.play(source)
        return True
    except Exception as e:
        print_error(e)
        return False


def pause_toggle() -> bool:
    global vlc_player

    try:
        vlc_player.pause_toggle()
        return True
    except Exception as e:
        print_error(e)
        return False


def stop() -> bool:
    global vlc_player

    try:
        vlc_player.stop()
        return True
    except Exception as e:
        print_error(e)
        return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='tts_service', help="thing name"
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
    tag_list = [
        MXTag(name='music'),
    ]
    function_list = [
        MXFunction(
            func=play,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=60,
            tag_list=tag_list,
            arg_list=[MXArgument(name='source', type=MXType.STRING, bound=(0, 10000))],
        ),
        MXFunction(
            func=pause_toggle,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=60,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=stop,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=60,
            tag_list=tag_list,
            arg_list=[],
        ),
    ]
    value_list = []

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
