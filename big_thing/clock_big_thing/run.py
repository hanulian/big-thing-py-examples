#!/bin/python

from big_thing_py.big_thing import *

import argparse
import datetime


def current_unix_time() -> float:
    return time.time()


def current_datetime() -> str:
    now = datetime.datetime.now()
    return f'{now.year:0>4}/{now.month:0>2}/{now.day:0>2}'


def current_time() -> str:
    now = datetime.datetime.now()
    return f'{now.hour:0>2}:{now.minute:0>2}:{now.second:0>2}'


def current_hour() -> int:
    now = datetime.datetime.now()
    return now.hour


def current_minute() -> int:
    now = datetime.datetime.now()
    return now.minute


def current_second() -> int:
    now = datetime.datetime.now()
    return now.second


def current_year() -> int:
    now = datetime.datetime.now()
    return now.year


def current_month() -> int:
    now = datetime.datetime.now()
    return now.month


def current_day() -> int:
    now = datetime.datetime.now()
    return now.day


def current_weekday() -> str:
    now = datetime.datetime.now()
    if now.weekday() == 0:
        return 'Monday'
    elif now.weekday() == 1:
        return 'Tuesday'
    elif now.weekday() == 2:
        return 'Wednesday'
    elif now.weekday() == 3:
        return 'Thursday'
    elif now.weekday() == 4:
        return 'Friday'
    elif now.weekday() == 5:
        return 'Saturday'
    elif now.weekday() == 6:
        return 'Sunday'


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='clock_big_thing', help="thing name")
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


def generate_thing(args):
    tag_list = [SoPTag(name='clock')]
    function_list = []
    value_list = [SoPValue(name='unix_time',
                           func=current_unix_time,
                           type=SoPType.DOUBLE,
                           bound=(0, 1999999999),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='datetime',
                           func=current_datetime,
                           type=SoPType.STRING,
                           bound=(0, 20),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='time',
                           func=current_time,
                           type=SoPType.STRING,
                           bound=(0, 20),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='hour',
                           func=current_hour,
                           type=SoPType.STRING,
                           bound=(0, 9999),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='minute',
                           func=current_minute,
                           type=SoPType.STRING,
                           bound=(0, 9999),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='second',
                           func=current_second,
                           type=SoPType.STRING,
                           bound=(0, 9999),
                           cycle=0.1,
                           tag_list=tag_list),
                  SoPValue(name='year',
                           func=current_year,
                           type=SoPType.INTEGER,
                           bound=(0, 9999),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='month',
                           func=current_month,
                           type=SoPType.INTEGER,
                           bound=(0, 12),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='day',
                           func=current_day,
                           type=SoPType.INTEGER,
                           bound=(0, 31),
                           cycle=1,
                           tag_list=tag_list),
                  SoPValue(name='weekday',
                           func=current_weekday,
                           type=SoPType.STRING,
                           bound=(0, 20),
                           cycle=1,
                           tag_list=tag_list)]

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
