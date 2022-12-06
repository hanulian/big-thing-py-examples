#!/bin/python

from big_thing_py.super_thing import *

import argparse


class SoPBasicSuperThing(SoPSuperThing):
    def __init__(self, name: str, service_list: List[SoPService] = ..., alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 refresh_cycle: float = 10):

        tag_list = [SoPTag(name='super'),
                    SoPTag(name='basic'),
                    SoPTag(name='big_thing'),
                    SoPTag(name='function')]
        int_arg = SoPArgument(name='int_arg',
                              type=SoPType.INTEGER,
                              bound=(0, 1000000))
        delay_arg = SoPArgument(name='delay_arg',
                                type=SoPType.DOUBLE,
                                bound=(0.0, 1000000.0))

        value_list = []
        function_list = [SoPSuperFunction(func=self.super_func_execute_func_no_arg_SINGLE,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_execute_func_no_arg_ALL,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_execute_func_with_arg_SINGLE,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[int_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_execute_func_with_arg_ALL,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[int_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_execute_func_with_arg_and_delay_SINGLE,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[int_arg, delay_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_execute_func_with_arg_and_delay_ALL,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[int_arg, delay_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_get_value_current_time_SINGLE,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_func_get_value_current_time_ALL,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_multiple_req_line1,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[
                                              int_arg, delay_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_multiple_req_line2,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[
                                              int_arg, delay_arg],
                                          timeout=300,
                                          energy=110),
                         SoPSuperFunction(func=self.super_multiple_req_line_with_fixed_argument,
                                          return_type=SoPType.INTEGER,
                                          tag_list=tag_list,
                                          arg_list=[
                                              int_arg, delay_arg],
                                          timeout=300,
                                          energy=110), ]

        service_list = value_list + function_list
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port,
                         ssl_ca_path, ssl_enable, log_name, log_enable, log_mode, append_mac_address, refresh_cycle)

    def super_func_execute_func_no_arg_SINGLE(self, key) -> int:
        result_list = self.req(key, subfunction_name='func_no_arg', tag_list=['basic'],
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_no_arg_ALL(self, key) -> int:
        result_list = self.req(key, subfunction_name='func_no_arg', tag_list=['basic'],
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_SINGLE(self, key, int_arg: int) -> int:
        result_list = self.req(key, subfunction_name='func_with_arg', tag_list=['basic'], arg_list=(int_arg, ),
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_ALL(self, key, int_arg: int) -> int:
        result_list = self.req(key, subfunction_name='func_with_arg', tag_list=['basic'], arg_list=(int_arg, ),
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_and_delay_SINGLE(self, key, int_arg: int, delay: float) -> int:
        result_list = self.req(key, subfunction_name='func_with_arg_and_delay', tag_list=['basic'], arg_list=(int_arg, delay, ),
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_execute_func_with_arg_and_delay_ALL(self, key, int_arg: int, delay: float) -> int:
        result_list = self.req(key, subfunction_name='func_with_arg_and_delay', tag_list=['basic'], arg_list=(int_arg, delay, ),
                               service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_SINGLE(self, key) -> int:
        result_list = self.req(key, subfunction_name='value_current_time', tag_list=['basic'],
                               service_type=SoPServiceType.VALUE, policy=SoPPolicy.SINGLE)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_func_get_value_current_time_ALL(self, key) -> int:
        result_list = self.req(key, subfunction_name='value_current_time', tag_list=['basic'],
                               service_type=SoPServiceType.VALUE, policy=SoPPolicy.ALL)

        result_sum = 0
        if result_list:
            for result in result_list:
                result_sum += result['return_value']

            return result_sum
        else:
            return 0

    def super_multiple_req_line1(self, key, int_arg: int, delay: float) -> int:
        result_list1 = self.req(key, subfunction_name='func_with_arg_and_delay', tag_list=['basic'], arg_list=(int_arg, delay, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)
        result_list2 = self.req(key, subfunction_name='func_with_arg', tag_list=['basic'], arg_list=(int_arg, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)
        result_list3 = self.req(key, subfunction_name='func_no_arg', tag_list=['basic'], arg_list=(),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

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

    def super_multiple_req_line2(self, key, int_arg: int, delay: float) -> int:
        result_list1 = self.req(key, subfunction_name='func_with_arg_and_delay', tag_list=['basic'], arg_list=(int_arg, delay, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)
        result_list2 = self.req(key, subfunction_name='func_with_arg', tag_list=['basic'], arg_list=(int_arg, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)
        result_list3 = self.req(key, subfunction_name='func_no_arg', tag_list=['basic'], arg_list=(),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.ALL)

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

    def super_multiple_req_line_with_fixed_argument(self, key, int_arg: int, delay: float) -> int:
        result_list1 = self.req(key, subfunction_name='func_with_arg', tag_list=['basic'], arg_list=(int_arg, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)
        result_list2 = self.req(key, subfunction_name='func_with_arg_and_delay', tag_list=['basic'], arg_list=(142, delay, ),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)
        result_list3 = self.req(key, subfunction_name='func_no_arg', tag_list=['basic'], arg_list=(),
                                service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.SINGLE)

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
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='super_feature_big_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--refresh_cycle", '-rc', action='store', type=int,
                        required=False, default=5, help="refresh cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    parser.add_argument("--log_mode", action='store',
                        required=False, default=SoPPrintMode.FULL, help="log mode")
    parser.add_argument("--append_mac", '-am', action='store_true',                         # store_true, store_false
                        required=False, help="append mac address to thing name")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    super_thing = SoPBasicSuperThing(name=args.name, ip=args.host, port=args.port,
                                     alive_cycle=args.alive_cycle, refresh_cycle=args.refresh_cycle, log_mode=SoPPrintMode.FULL)
    return super_thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
