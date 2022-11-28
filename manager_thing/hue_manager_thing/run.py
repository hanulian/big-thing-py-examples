from hue_manager_thing import *
from hue_staff_thing import *

import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='hue_manager_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', dest='log',
                        required=False, default=True, help="log enable")

    parser.add_argument("--endpoint", '-ep', action='store', type=str,
                        required=False, default='', help="endpoint")
    parser.add_argument("--api_token", '-k', action='store', type=str,
                        required=False, default='', help="api token")
    parser.add_argument("--scan_cycle", '-sc', action='store', type=int,
                        required=False, default=60, help="scan cycle")
    parser.add_argument("--config", '-c', action='store', type=str,
                        required=False, default='', help="config file path")
    parser.add_argument("--config_select", '-s', action='store', type=str,
                        required=False, default='', help="config select")
    parser.add_argument("--manager_mode", '-md', action='store', type=str,
                        required=False, default=SoPManagerMode.SPLIT.value, help="manager_mode")
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def generate_thing(args) -> SoPHueManagerThing:
    thing = SoPHueManagerThing(name=args.name, ip=args.host, port=args.port,
                               alive_cycle=args.alive_cycle, service_list=[],
                               manager_mode=args.manager_mode, scan_cycle=args.scan_cycle,
                               conf_file_path=args.config, conf_select=args.config_select)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
