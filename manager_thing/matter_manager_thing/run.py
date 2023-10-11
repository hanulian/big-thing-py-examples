from matter_manager_thing import *
from matter_staff_thing import *

import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='hue_manager_thing', help="thing name"
    )
    parser.add_argument(
        "--host", '-ip', action='store', type=str, required=False, default='127.0.0.1', help="host name"
    )
    parser.add_argument("--port", '-p', action='store', type=int, required=False, default=1883, help="port")
    parser.add_argument(
        "--alive_cycle", '-ac', action='store', type=int, required=False, default=60, help="alive cycle"
    )
    parser.add_argument("--auto_scan", '-as', action='store_true', required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', dest='log', required=False, default=True, help="log enable")
    parser.add_argument("--scan_cycle", '-sc', action='store', type=int, required=False, default=60, help="scan cycle")
    parser.add_argument(
        "--config", '-c', action='store', type=str, required=False, default='config.json', help="config file path"
    )
    parser.add_argument(
        "--config_select", '-s', action='store', type=str, required=False, default='', help="config select"
    )
    parser.add_argument(
        "--manager_mode",
        '-md',
        action='store',
        type=str,
        required=False,
        default=MXManagerMode.SPLIT.value,
        help="manager_mode",
    )
    parser.add_argument(
        "--ssid",
        action='store',
        type=str,
        required=False,
        default='',
        help="wifi ssid",
    )
    parser.add_argument(
        "--password",
        action='store',
        type=str,
        required=False,
        default='',
        help="wifi password",
    )
    parser.add_argument(
        "--dataset",
        action='store',
        type=str,
        required=False,
        default='',
        help="thread dataset",
    )
    parser.add_argument(
        "--matter-server-clean-start",
        dest='matter_server_clean_start',
        action='store_true',
        required=False,
        help="matter server clean start",
    )
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def generate_thing(args) -> MXMatterManagerThing:
    thing = MXMatterManagerThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        service_list=[],
        manager_mode=args.manager_mode,
        scan_cycle=args.scan_cycle,
        conf_file_path=args.config,
        conf_select=args.config_select,
        wifi_credentials=(args.ssid, args.password),
        thread_network_dataset=args.dataset,
        matter_server_clean_start=args.matter_server_clean_start,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
