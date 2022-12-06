#!/bin/python

import argparse
from datetime import datetime
from platform import uname
from big_thing_py.big_thing import *

import cv2


def camera_capture(image_name: str, cam_num: int = 0):
    try:
        ret = False
        if uname().system == 'Darwin':
            cam = cv2.VideoCapture(cam_num)
            curr_time = time.time()
            while time.time() - curr_time < 0.1:
                ret, frame = cam.read()
                cv2.waitKey(30)
                cv2.imwrite(image_name, frame)
        elif uname().system == 'Windows':
            cam = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
            ret, frame = cam.read()
            cv2.imwrite(image_name, frame)
            cam.release()
        else:
            cam = cv2.VideoCapture(cam_num)
            ret, frame = cam.read()
            cv2.imwrite(image_name, frame)
            cam.release()
    except Exception as e:
        print_error(e)
        return False

    return ret


def capture() -> str:
    formattedDate = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'{formattedDate}.jpg'
    result = camera_capture(file_name, 0)
    if result:
        return os.path.abspath(file_name)
    else:
        return '실패'


def capture_with_filename(file_name: str) -> str:
    result = camera_capture(file_name, 0)
    if result:
        return os.path.abspath(file_name)
    else:
        return '실패'


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='camera_big_thing', help="thing name")
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
    tag_list = [SoPTag(name='camera')]
    function_list = [SoPFunction(func=capture,
                                 exec_time=300,
                                 timeout=300,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[]),
                     SoPFunction(func=capture_with_filename,
                                 exec_time=300,
                                 timeout=300,
                                 return_type=SoPType.STRING,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='image_name_arg',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
