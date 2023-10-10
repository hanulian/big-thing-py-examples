#!/bin/python

from big_thing_py.super_thing import *

import argparse


class MXTestbedSuperThing(MXSuperThing):
    professor_exist_map = {}

    def __init__(
        self,
        name: str = MXSuperThing.DEFAULT_NAME,
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        is_super: bool = True,
        is_parallel: bool = True,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_enable: bool = False,
        log_name: str = None,
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
        refresh_cycle: float = 30,
    ):
        tag_list = [MXTag(name='super'), MXTag(name='testbed')]

        value_list = []
        function_list = [
            MXSuperFunction(
                func=self.alert_all,
                return_type=MXType.INTEGER,
                exec_time=10,
                timeout=10,
                tag_list=tag_list,
                arg_list=[],
                energy=110,
            ),
            MXSuperFunction(
                func=self.update_professor_exist,
                return_type=MXType.INTEGER,
                exec_time=1,
                timeout=1,
                tag_list=tag_list,
                arg_list=[
                    MXArgument(name='professor_name', type=MXType.STRING, bound=(0, 10000)),
                    MXArgument(name='exist', type=MXType.BOOL, bound=(0, 2)),
                ],
                energy=110,
            ),
            MXSuperFunction(
                func=self.get_professor_exist,
                return_type=MXType.INTEGER,
                exec_time=0.5,
                timeout=0.5,
                tag_list=tag_list,
                arg_list=[MXArgument(name='professor_name', type=MXType.STRING, bound=(0, 10000))],
                energy=110,
            ),
        ]

        service_list = value_list + function_list
        super().__init__(
            name=name,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=is_super,
            is_parallel=is_parallel,
            ip=ip,
            port=port,
            ssl_ca_path=ssl_ca_path,
            ssl_enable=ssl_enable,
            log_name=log_name,
            log_enable=log_enable,
            log_mode=log_mode,
            append_mac_address=append_mac_address,
            refresh_cycle=refresh_cycle,
        )

    # TODO: 만약 alert thing이 구현 되면 함수 내용을 바꿔야함
    def alert_all(self, key) -> int:
        result_list = self.req(
            key,
            sub_service_name='alert',
            tag_list=['alert'],
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )

        # TODO: 추후에 return_value -> return_values로 바꿔야함
        result_list = [result['return_value'] for result in result_list]
        return all(result_list)

    def update_professor_exist(self, key, professor_name: str, exist: bool) -> bool:
        MXTestbedSuperThing.professor_exist_map[professor_name] = bool(exist)

    def get_professor_exist(self, key, professor_name: str) -> bool:
        try:
            exist = MXTestbedSuperThing.professor_exist_map[professor_name]
            return exist
        except KeyError:
            return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='super_feature_big_thing', help="thing name"
    )
    parser.add_argument(
        "--host", '-ip', action='store', type=str, required=False, default='127.0.0.1', help="host name"
    )
    parser.add_argument("--port", '-p', action='store', type=int, required=False, default=1883, help="port")
    parser.add_argument(
        "--alive_cycle", '-ac', action='store', type=int, required=False, default=60, help="alive cycle"
    )
    parser.add_argument(
        "--refresh_cycle", '-rc', action='store', type=int, required=False, default=5, help="refresh cycle"
    )
    parser.add_argument("--auto_scan", '-as', action='store_true', required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true', required=False, help="log enable")
    parser.add_argument("--log_mode", action='store', required=False, default=MXPrintMode.FULL, help="log mode")
    parser.add_argument(
        "--append_mac",
        '-am',
        action='store_true',  # store_true, store_false
        required=False,
        help="append mac address to thing name",
    )
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    super_thing = MXTestbedSuperThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        refresh_cycle=args.refresh_cycle,
        log_mode=MXPrintMode.FULL,
    )
    return super_thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
