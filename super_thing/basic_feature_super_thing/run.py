#!/bin/python

from big_thing_py.super_thing import *

import argparse


class MXBasicSuperThing(MXSuperThing):
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
        tag_list = [MXTag(name='super'), MXTag(name='basic'), MXTag(name='big_thing')]
        int_arg = MXArgument(name='int_arg', type=MXType.INTEGER, bound=(0, 1000000))
        delay_arg = MXArgument(name='delay_arg', type=MXType.DOUBLE, bound=(0.0, 1000000.0))

        value_list = []
        function_list = [
            MXSuperFunction(
                func=self.super_func_execute_func_no_arg_SINGLE,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_execute_func_no_arg_ALL,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_execute_func_with_arg_SINGLE,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_execute_func_with_arg_ALL,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_execute_func_with_arg_and_delay_SINGLE,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_execute_func_with_arg_and_delay_ALL,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_get_value_current_time_SINGLE,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_func_get_value_current_time_ALL,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_multiple_sub_service_request_SINGLE,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_multiple_sub_service_request_ALL,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_multiple_sub_service_request_with_fixed_argument1,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_multiple_sub_service_request_with_fixed_argument2,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
                energy=110,
            ),
            MXSuperFunction(
                func=self.super_multiple_sub_service_request_with_argument_pass,
                return_type=MXType.INTEGER,
                tag_list=tag_list,
                arg_list=[int_arg, delay_arg],
                timeout=300,
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

    def super_func_execute_func_no_arg_SINGLE(self) -> int:
        result_list = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_no_arg_ALL(self) -> int:
        result_list = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_SINGLE(self, int_arg: int) -> int:
        result_list = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_ALL(self, int_arg: int) -> int:
        result_list = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_and_delay_SINGLE(self, int_arg: int, delay: float) -> int:
        result_list = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                int_arg,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_and_delay_ALL(self, int_arg: int, delay: float) -> int:
        result_list = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                int_arg,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_SINGLE(self) -> int:
        result_list = self.req(
            sub_service_name='value_current_time',
            tag_list=['basic'],
            return_type=MXType.INTEGER,
            service_type=MXServiceType.VALUE,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_ALL(self) -> int:
        result_list = self.req(
            sub_service_name='value_current_time',
            tag_list=['basic'],
            return_type=MXType.INTEGER,
            service_type=MXServiceType.VALUE,
            range_type=MXRangeType.ALL,
        )

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_sub_service_request_SINGLE(self, int_arg: int, delay: float) -> int:
        result_list1 = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                int_arg,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result_list2 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result_list3 = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            arg_list=(),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list1 and result_list2 and result_list3:
            for result in result_list1:
                result_sum += result['return_value']
            for result in result_list2:
                result_sum += result['return_value']
            for result in result_list3:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_sub_service_request_ALL(self, int_arg: int, delay: float) -> int:
        result_list1 = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                int_arg,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )
        result_list2 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )
        result_list3 = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            arg_list=(),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )

        result_sum = 0
        if result_list1 and result_list2 and result_list3:
            for result in result_list1:
                result_sum += result['return_value']
            for result in result_list2:
                result_sum += result['return_value']
            for result in result_list3:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_sub_service_request_with_fixed_argument1(self, int_arg: int, delay: float) -> int:
        result_list1 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result_list2 = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                142,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result_list3 = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            arg_list=(),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list1 and result_list2 and result_list3:
            for result in result_list1:
                result_sum += result['return_value']
            for result in result_list2:
                result_sum += result['return_value']
            for result in result_list3:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_sub_service_request_with_fixed_argument2(self, int_arg: int, delay: float) -> int:
        result_list1 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result_list2 = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                142,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )
        result_list3 = self.req(
            sub_service_name='func_no_arg',
            tag_list=['basic'],
            arg_list=(),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list1 and result_list2 and result_list3:
            for result in result_list1:
                result_sum += result['return_value']
            for result in result_list2:
                result_sum += result['return_value']
            for result in result_list3:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_sub_service_request_with_argument_pass(self, int_arg: int, delay: float) -> int:
        result_list1 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(int_arg,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )
        result1 = result_list1[0]['return_value'] if result_list1 else 0
        result_list2 = self.req(
            sub_service_name='func_with_arg_and_delay',
            tag_list=['basic'],
            arg_list=(
                result1,
                delay,
            ),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.ALL,
        )
        result_list3 = self.req(
            sub_service_name='func_with_arg',
            tag_list=['basic'],
            arg_list=(100,),
            return_type=MXType.INTEGER,
            service_type=MXServiceType.FUNCTION,
            range_type=MXRangeType.SINGLE,
        )

        result_sum = 0
        if result_list1 and result_list2 and result_list3:
            for result in result_list1:
                result_sum += result['return_value']
            for result in result_list2:
                result_sum += result['return_value']
            for result in result_list3:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    # def super_func_req_scenario_line(self, scenario_line: str) -> bool:
    #     result_list = self.r(scenario_line)
    #     # result_list = self.r('(#Hue).on()')
    #     # result_list = self.r('(#Hue).set_brightness($1)', 100)
    #     # result_list = self.r('(#Hue).off()')

    #     return result_list


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


def generate_thing(args):
    super_thing = MXBasicSuperThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        refresh_cycle=args.refresh_cycle,
        log_mode=MXPrintMode.get(args.log_mode),
        append_mac_address=args.append_mac,
    )
    return super_thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
