#!/bin/python

from big_thing_py.big_thing import *

import argparse
import requests
from bs4 import BeautifulSoup
import datetime


def get_menu(url):
    response = requests.get(url)
    result = {}

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        whole_menu = soup.select('body > div.content > div > div[class="restaurant"]')

        key = None
        for menu in whole_menu:
            # restaurant01 > div > div.meals > div.meal.lunch > div:nth-child(2) > div.menu-name-with-price > a
            try:
                locate = menu.select_one('div[class="restaurant-name"] > a').get('data-resname')
                whole_meals = menu.select_one('div[class="meals"]')
                breakfasts = whole_meals.select(
                    'div[class="meal breakfast"] > div[class="menu"] > div.menu-name-with-price > a'
                )
                breakfasts = [breakfast.get('data-menu') for breakfast in breakfasts]

                lunchs = whole_meals.select(
                    'div[class="meal lunch"] > div[class="menu"] > div.menu-name-with-price > a'
                )
                lunchs = [lunch.get('data-menu') for lunch in lunchs]

                dinners = whole_meals.select(
                    'div[class="meal dinner"] > div[class="menu"] > div.menu-name-with-price > a'
                )
                dinners = [dinner.get('data-menu') for dinner in dinners]

                result[locate] = dict(breakfast=breakfasts, lunch=lunchs, dinner=dinners)

            except KeyError:
                pass

    return result


def menu(command: str) -> str:
    try:
        menu = None
        command_list = command.split()
        date = command_list[0]
        locate = command_list[1]
        time = command_list[2]

        now = datetime.date.today()
        if date == '오늘':
            whole_menu = get_menu(f'https://snumenu.gerosyab.net/ko/menus?date={str(now)}')
        elif date == '내일':
            whole_menu = get_menu(f'https://snumenu.gerosyab.net/ko/menus?date={str(now + datetime.timedelta(days=1))}')
        else:
            error_message = '메뉴는 오늘, 내일만 조회가 가능합니다.'
            return error_message

        for key, value in whole_menu.items():
            if locate in key:
                if time == '아침':
                    menu = value['breakfast']
                if time == '점심':
                    menu = value['lunch']
                if time == '저녁':
                    menu = value['dinner']
            else:
                pass
    except Exception as e:
        error_message = f'잘못된 입력입니다(입력 예: 오늘 301동 점심). 사용자 입력: {command}'
        return error_message

    if menu is None:
        return f'해당 식당의 {time} 메뉴를 조회할 수 없습니다.'
    else:
        result = '\n'.join(menu)
        return result


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='menu_parser_big_thing', help="thing name"
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
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [MXTag(name='menu')]
    function_list = [
        MXFunction(
            func=menu,
            return_type=MXType.STRING,
            tag_list=tag_list,
            timeout=5,
            exec_time=5,
            arg_list=[MXArgument(name='command', type=MXType.STRING, bound=(0, 1000))],
        )
    ]
    value_list = []

    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        service_list=function_list + value_list,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
