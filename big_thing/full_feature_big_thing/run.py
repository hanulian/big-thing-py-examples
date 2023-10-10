from big_thing_py.big_thing import *

import time
import random
import argparse


# ----------------------------------------------------------------------------------------------------------------------


def fail_function() -> int:
    raise Exception('fail function')


@static_vars(int_value=0)
def int_function_no_arg_timeout_3() -> int:
    int_function_no_arg_timeout_3.int_value += 1

    time.sleep(5)

    MXLOG_DEBUG(f'{get_current_function_name()} run. return {int_function_no_arg_timeout_3.int_value}', 'green')
    return int_function_no_arg_timeout_3.int_value


@static_vars(int_value=0)
def int_function_no_arg_with_delay_1() -> int:
    int_function_no_arg_with_delay_1.int_value += 1

    time.sleep(1)

    MXLOG_DEBUG(f'{get_current_function_name()} run. return {int_function_no_arg_with_delay_1.int_value}', 'green')
    return int_function_no_arg_with_delay_1.int_value


def int_function_return_fixed_5() -> int:
    MXLOG_DEBUG(f'{get_current_function_name()} run. return {5}', 'green')
    return 5


# ----------------------------------------------------------------------------------------------------------------------


@static_vars(int_value=0)
def int_function_no_arg() -> int:
    int_function_no_arg.int_value += 1
    MXLOG_DEBUG(f'{get_current_function_name()} run. return {int_function_no_arg.int_value}', 'green')
    return int_function_no_arg.int_value


@static_vars(float_value=0.0)
def float_function_no_arg() -> float:
    float_function_no_arg.float_value += 1.0
    MXLOG_DEBUG(f'{get_current_function_name()} run. return {float_function_no_arg.float_value}', 'green')
    return float_function_no_arg.float_value


@static_vars(str_value='0')
def str_function_no_arg() -> str:
    str_function_no_arg.str_value = str(int(str_function_no_arg.str_value) + 1)
    MXLOG_DEBUG(f'{get_current_function_name()} run. return {str_function_no_arg.str_value}', 'green')
    return str_function_no_arg.str_value


@static_vars(bool_value=False)
def bool_function_no_arg() -> bool:
    bool_function_no_arg.bool_value = bool_function_no_arg.bool_value % 2 == 0
    MXLOG_DEBUG(f'{get_current_function_name()} run. return {bool_function_no_arg.bool_value}', 'green')
    return bool_function_no_arg.bool_value


@static_vars(binary_value='0')
def binary_function_no_arg() -> str:
    binary_function_no_arg.binary_value = str(int(binary_function_no_arg.binary_value) + 1)
    MXLOG_DEBUG(
        f'{get_current_function_name()} run. return {string_to_base64(binary_function_no_arg.binary_value)} --> ("{binary_function_no_arg.binary_value}")',
        'green',
    )
    return string_to_base64(binary_function_no_arg.binary_value)


def void_function_no_arg() -> None:
    MXLOG_DEBUG(f'{get_current_function_name()} run. no return', 'green')


# ----------------------------------------------------------------------------------------------------------------------


def int_function_with_arg(int_arg: int) -> int:
    MXLOG_DEBUG(f'{get_current_function_name()} run. argument : {int_arg}, return {int_arg}', 'green')
    return int_arg


def float_function_with_arg(float_arg: float) -> float:
    MXLOG_DEBUG(f'{get_current_function_name()} run. argument : {float_arg}, return {float_arg}', 'green')
    return float_arg


def str_function_with_arg(str_arg: str) -> str:
    MXLOG_DEBUG(f'{get_current_function_name()} run. argument : {str_arg}, return {str_arg}', 'green')
    return str_arg


def bool_function_with_arg(bool_arg: bool) -> bool:
    MXLOG_DEBUG(f'{get_current_function_name()} run. argument : {bool_arg}, return {bool_arg}', 'green')
    return bool_arg


def binary_function_with_arg(binary_arg: str) -> str:
    MXLOG_DEBUG(
        f'{get_current_function_name()} run. argument : {binary_arg} --> ("{base64_to_string(binary_arg)}"), return {binary_arg} --> ("{base64_to_string(binary_arg)}")',
        'green',
    )
    return binary_arg


def void_function_with_arg(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool, binary_arg: str) -> None:
    MXLOG_DEBUG(
        f'{get_current_function_name()} run. argument : {int_arg}, {float_arg}, {str_arg}, {bool_arg}, {binary_arg} no return.',
        'green',
    )


# ----------------------------------------------------------------------------------------------------------------------


def generate_thing(args) -> MXBigThing:
    alive_cycle = 60
    value_cycle = alive_cycle

    tag_list = [MXTag('full')]

    int_arg_list = [
        MXArgument(name='int_arg', type=MXType.INTEGER, bound=(-2147483648, 2147483647)),
    ]
    float_arg_list = [
        MXArgument(name='float_arg', type=MXType.DOUBLE, bound=(-2147483648, 2147483647)),
    ]
    str_arg_list = [
        MXArgument(name='str_arg', type=MXType.STRING, bound=(-2147483648, 2147483647)),
    ]
    bool_arg_list = [
        MXArgument(name='bool_arg', type=MXType.BOOL, bound=(-2147483648, 2147483647)),
    ]
    binary_arg_list = [MXArgument(name='binary_arg', type=MXType.BINARY, bound=(-2147483648, 2147483647))]
    full_arg_list = [
        MXArgument(name='int_arg', type=MXType.INTEGER, bound=(-2147483648, 2147483647)),
        MXArgument(name='float_arg', type=MXType.DOUBLE, bound=(-2147483648, 2147483647)),
        MXArgument(name='str_arg', type=MXType.STRING, bound=(-2147483648, 2147483647)),
        MXArgument(name='bool_arg', type=MXType.BOOL, bound=(-2147483648, 2147483647)),
        MXArgument(name='binary_arg', type=MXType.BINARY, bound=(-2147483648, 2147483647)),
    ]

    value_list = [
        MXValue(
            name='int_value_5',
            func=int_function_return_fixed_5,
            type=MXType.INTEGER,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('INTEGER')],
            cycle=1,
        ),
        MXValue(
            name='int_value',
            func=int_function_no_arg,
            type=MXType.INTEGER,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('INTEGER')],
            cycle=1,
        ),
        MXValue(
            name='float_value',
            func=float_function_no_arg,
            type=MXType.DOUBLE,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('DOUBLE')],
            cycle=1,
        ),
        MXValue(
            name='str_value',
            func=str_function_no_arg,
            type=MXType.STRING,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('STRING')],
            cycle=1,
        ),
        MXValue(
            name='bool_value',
            func=bool_function_no_arg,
            type=MXType.BOOL,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('BOOL')],
            cycle=1,
        ),
        MXValue(
            name='binary_value',
            func=binary_function_no_arg,
            type=MXType.BINARY,
            bound=(-2147483648, 2147483647),
            tag_list=tag_list + [MXTag('BINARY')],
            cycle=1,
        ),
    ]

    no_arg_function_list = [
        MXFunction(func=fail_function, return_type=MXType.INTEGER, tag_list=tag_list + [MXTag('INTEGER')], arg_list=[]),
        MXFunction(
            func=int_function_no_arg_timeout_3,
            return_type=MXType.INTEGER,
            tag_list=tag_list + [MXTag('INTEGER')],
            arg_list=[],
            timeout=3,
        ),
        MXFunction(
            func=int_function_no_arg_with_delay_1,
            return_type=MXType.INTEGER,
            tag_list=tag_list + [MXTag('INTEGER')],
            arg_list=[],
        ),
        MXFunction(
            func=int_function_no_arg, return_type=MXType.INTEGER, tag_list=tag_list + [MXTag('INTEGER')], arg_list=[]
        ),
        MXFunction(
            func=float_function_no_arg, return_type=MXType.DOUBLE, tag_list=tag_list + [MXTag('DOUBLE')], arg_list=[]
        ),
        MXFunction(
            func=str_function_no_arg, return_type=MXType.STRING, tag_list=tag_list + [MXTag('STRING')], arg_list=[]
        ),
        MXFunction(
            func=bool_function_no_arg, return_type=MXType.BOOL, tag_list=tag_list + [MXTag('BOOL')], arg_list=[]
        ),
        MXFunction(
            func=binary_function_no_arg,
            return_type=MXType.BINARY,
            desc='binary_function_no_arg',
            tag_list=tag_list + [MXTag('BINARY')],
            arg_list=[],
        ),
        MXFunction(
            func=void_function_no_arg, return_type=MXType.VOID, tag_list=tag_list + [MXTag('VOID')], arg_list=[]
        ),
    ]
    arg_function_list = [
        MXFunction(
            name='int_function_with_arg',
            func=int_function_with_arg,
            return_type=MXType.INTEGER,
            desc='int_function_with_arg',
            tag_list=tag_list + [MXTag('INTEGER')],
            arg_list=int_arg_list,
        ),
        MXFunction(
            name='float_function_with_arg',
            func=float_function_with_arg,
            return_type=MXType.DOUBLE,
            desc='float_function_with_arg',
            tag_list=tag_list + [MXTag('DOUBLE')],
            arg_list=float_arg_list,
        ),
        MXFunction(
            name='str_function_with_arg',
            func=str_function_with_arg,
            return_type=MXType.STRING,
            desc='str_function_with_arg',
            tag_list=tag_list + [MXTag('STRING')],
            arg_list=str_arg_list,
        ),
        MXFunction(
            name='bool_function_with_arg',
            func=bool_function_with_arg,
            return_type=MXType.BOOL,
            desc='bool_function_with_arg',
            tag_list=tag_list + [MXTag('BOOL')],
            arg_list=bool_arg_list,
        ),
        MXFunction(
            name='binary_function_with_arg',
            func=binary_function_with_arg,
            return_type=MXType.BINARY,
            desc='binary_function_with_arg',
            tag_list=tag_list + [MXTag('BINARY')],
            arg_list=binary_arg_list,
        ),
        MXFunction(
            name='void_function_with_arg',
            func=void_function_with_arg,
            return_type=MXType.VOID,
            desc='void_function_with_arg',
            tag_list=tag_list + [MXTag('VOID')],
            arg_list=full_arg_list,
        ),
    ]
    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        service_list=value_list + no_arg_function_list + arg_function_list,
        log_mode=MXPrintMode.get(args.log_mode),
    )
    return thing


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='full_feature_big_thing', help="thing name"
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
    args, unknown = parser.parse_known_args()

    return args


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
