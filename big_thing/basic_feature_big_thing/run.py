from big_thing_py.big_thing import *

import time
import random
import argparse


def func_no_arg() -> int:
    return_value = random.randint(0, 100)
    SOPLOG_DEBUG(
        f'{get_current_function_name()} run... return: {return_value}')
    return return_value


def func_with_arg(int_arg: int) -> bool:
    return_value = int_arg
    SOPLOG_DEBUG(
        f'{get_current_function_name()} run... return: {return_value}')
    return return_value


def func_with_arg_and_delay(int_arg: int, deley: float) -> int:
    return_value = int_arg
    SOPLOG_DEBUG(
        f'{get_current_function_name()} run... return: {return_value}')
    SOPLOG_DEBUG(f'deley : {deley}')
    time.sleep(deley)
    return return_value


def value_current_time():
    return_value = int(get_current_time())
    SOPLOG_DEBUG(f'{get_current_function_name()} run! return: {return_value}')
    return return_value


def generate_thing(args):
    tag_list = [SoPTag(name='basic'),
                SoPTag(name='big_thing')]
    arg_list = [SoPArgument(name='int_arg',
                            type=SoPType.INTEGER,
                            bound=(0, 10000))]
    delay_arg = SoPArgument(name='delay_arg',
                            type=SoPType.DOUBLE,
                            bound=(0, 10000))
    function_list = [SoPFunction(func=func_no_arg,
                                 return_type=SoPType.INTEGER,
                                 tag_list=tag_list,
                                 arg_list=[],
                                 energy=45),
                     SoPFunction(func=func_with_arg,
                                 return_type=SoPType.INTEGER,
                                 tag_list=tag_list,
                                 arg_list=arg_list,
                                 energy=12),
                     SoPFunction(func=func_with_arg_and_delay,
                                 return_type=SoPType.INTEGER,
                                 timeout=10 * 1000,
                                 tag_list=tag_list + [delay_arg],
                                 arg_list=arg_list + [delay_arg],
                                 energy=56)]
    value_list = [SoPValue(func=value_current_time,
                           type=SoPType.INTEGER,
                           bound=(0, 2147483647),
                           tag_list=tag_list,
                           cycle=10)]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='basic_feature_big_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=11083, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def main():
    thing = generate_thing(arg_parse())
    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()
