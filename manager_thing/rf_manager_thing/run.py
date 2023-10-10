from rf_manager_thing import *
import argparse

# rf_radio = RF24(22, 0)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='rf_manager_thing', help="thing name"
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

    parser.add_argument("--scan_cycle", '-sc', action='store', type=int, required=False, default=60, help="scan_cycle")
    parser.add_argument(
        "--mode",
        '-md',
        action='store',
        type=str,
        required=False,
        default=MXManagerMode.SPLIT.value,
        help="manager mode",
    )
    arg_list, unknown = parser.parse_known_args()

    return arg_list


def generate_thing(args):
    thing = MXRFManagerThing(
        name=args.name,
        port=args.port,
        ip=args.host,
        network_type=MXNetworkType.RF,
        mode=MXManagerMode.JOIN,
        addresses=(0xFFFFFFFFFFF1, 0xFFFFFFFFFFF0),
        power_mode=MXRFPowerMode.HIGH,
        alive_cycle=args.alive_cycle,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
