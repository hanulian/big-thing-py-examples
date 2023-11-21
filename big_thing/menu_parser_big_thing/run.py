#!/bin/python

from big_thing_py.big_thing import *

import argparse
import requests
from bs4 import BeautifulSoup
import datetime
import random


LOCATION_LIST = [
    '학생식당',
    '전망대(3식당)',
    '기숙사식당',
    '302동식당',
    '301동식당',
    '동원관식당(113동)',
    '자하연식당',
    '투굿(공대간이식당)',
    '예술계식당(아름드리)',
    '웰스토리(220동)',
    '두레미담',
    '아워홈',
]


def find_location(input: str) -> Union[str, bool]:
    for location in LOCATION_LIST:
        if input in location:
            return location
    return False


def check_time_of_day() -> str:
    current_time = datetime.datetime.now().time()
    morning_start = datetime.time(5, 0)
    lunch_start = datetime.time(11, 0)
    evening_start = datetime.time(17, 0)

    if morning_start <= current_time < lunch_start:
        return "아침"
    elif lunch_start <= current_time < evening_start:
        return "점심"
    else:
        return "저녁"


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


def menu(command: str) -> Union[List[str], str]:
    try:
        menu: List[str] = None
        msg = ''
        command_list = command.split()
        date = command_list[0]
        locate = find_location(command_list[1])
        time = command_list[2]

        now = datetime.date.today()
        if date == '오늘':
            whole_menu = get_menu(f'https://snumenu.gerosyab.net/ko/menus?date={str(now)}')
        elif date == '내일':
            whole_menu = get_menu(f'https://snumenu.gerosyab.net/ko/menus?date={str(now + datetime.timedelta(days=1))}')
        else:
            msg = '날짜는 오늘, 내일만 조회가 가능합니다.'
            MXLOG_DEBUG(msg)
            return msg

        if not locate:
            msg = '식당 이름을 정확히 입력해주세요.'
            MXLOG_DEBUG(msg)
            return msg

        for key, value in whole_menu.items():
            if locate in key:
                # if time == '아침':
                #     menu = value['breakfast']
                if time == '점심':
                    menu = value['lunch']
                if time == '저녁':
                    menu = value['dinner']
                break
        else:
            msg = f'식당 {locate}은 존재하지 않습니다.'
            MXLOG_DEBUG(msg)
            return msg
    except Exception as e:
        msg = f'잘못된 입력입니다(입력 예: 오늘 301동 점심). 사용자 입력: {command}'
        MXLOG_DEBUG(msg)
        return msg

    if menu is None:
        return -1
    elif len(menu) == 0:
        return -2

    pruned_menu: List[str] = []
    for i, m in enumerate(menu):
        if '회' in m:
            continue
        pruned_m = (
            m.replace('<br>', '')
            .replace('*', ', ')
            .replace('&', ', ')
            .replace('<', '')
            .replace('>', '')
            .replace('(', ' ')
            .replace(')', '')
        )
        pruned_menu.append(pruned_m)

    if len(pruned_menu) == 0:
        return -2
    else:
        selected_menu = random.choice(pruned_menu).strip()
        return selected_menu


def today_menu() -> str:
    date = '오늘'
    locate = random.choice(LOCATION_LIST)
    time = check_time_of_day()
    command = f'{date} {locate} {time}'

    selected_menu = menu(command)
    if selected_menu == -1:
        return '메뉴 정보를 불러오는 데 실패하였습니다.'
    elif selected_menu == -2:
        return '메뉴 정보가 없습니다.'
    else:
        locate = locate.replace('(', ' ').replace(')', '')
        return f'오늘 {time} 메뉴로는 {locate}에서 {selected_menu}을 추천합니다.'


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
    parser.add_argument(
        "--log_mode", action='store', type=str, required=False, default=MXPrintMode.ABBR.value, help="log mode"
    )
    parser.add_argument(
        "--append_mac", '-am', action='store_false', required=False, help="append mac address to thing name"
    )
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [
        MXTag(name='menu'),
        MXTag(name='big_thing'),
    ]
    function_list = [
        MXFunction(
            func=menu,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='command', type=MXType.STRING, bound=(0, 1000))],
        ),
        MXFunction(
            func=today_menu,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[],
        ),
    ]
    value_list = []

    thing = MXBigThing(
        name=args.name,
        ip=args.host,
        port=args.port,
        alive_cycle=args.alive_cycle,
        log_mode=MXPrintMode.get(args.log_mode),
        append_mac_address=args.append_mac,
        service_list=function_list + value_list,
    )
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
