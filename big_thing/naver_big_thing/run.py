#!/bin/python

from big_thing_py.big_thing import *
from big_thing_py.utils.api_util import *
from naver_api_client import NaverAPIClient
from secret import API_KEY, CLIENT_ID

import argparse


naver_apiclient = NaverAPIClient(client_id=CLIENT_ID, api_key=API_KEY)


def face_detect(image: str) -> str:
    global naver_apiclient
    return naver_apiclient.face_detect(image)


def face_detect_celebrity(image: str) -> str:
    global naver_apiclient
    return naver_apiclient.face_detect_celebrity(image)


def papago(text: str, src: str, dst: str) -> str:
    global naver_apiclient
    return naver_apiclient.papago(text, src, dst)


def papago_detect_lang(text: str) -> str:
    global naver_apiclient
    return naver_apiclient.papago_detect_lang(text)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='naver_big_thing', help="thing name"
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
    tag_list = [MXTag(name='naver')]
    function_list = [
        MXFunction(
            func=face_detect,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='image_path_arg', type=MXType.STRING, bound=(0, 10000))],
        ),
        MXFunction(
            func=face_detect_celebrity,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='image_path_arg', type=MXType.STRING, bound=(0, 10000))],
        ),
        MXFunction(
            func=papago,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[
                MXArgument(name='text_arg', type=MXType.STRING, bound=(0, 10000)),
                MXArgument(name='src_arg', type=MXType.STRING, bound=(0, 10000)),
                MXArgument(name='dst_arg', type=MXType.STRING, bound=(0, 10000)),
            ],
        ),
        MXFunction(
            func=papago_detect_lang,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[MXArgument(name='text_arg', type=MXType.STRING, bound=(0, 10000))],
        ),
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
