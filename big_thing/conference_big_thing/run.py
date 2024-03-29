from big_thing_py.big_thing import *

import argparse


def record_start() -> bool:
    pass


def record_end() -> bool:
    pass


def to_text(file: str) -> str:
    pass


def generate_thing(args):
    tag_list = [
        MXTag(name='conference'),
        MXTag(name='big_thing'),
    ]
    function_list = [
        MXFunction(
            func=record_start,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=record_end,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            func=to_text,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='file', type=MXType.STRING, bound=(0, 10000))],
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


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='conference_big_thing', help="thing name"
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
