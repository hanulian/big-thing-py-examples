#!/bin/python

from big_thing_py.big_thing import *

import argparse
import os
from gtts import gTTS
from langdetect import detect
import platform
import shutil


def pkg_install(package):
    import pip

    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def speak(text: str) -> bool:
    try:
        lang = detect(text)
        MXLOG_DEBUG(f'lang detected: {lang}')

        myobj = gTTS(text=text, lang=lang, slow=False)
        file_name = 'temp.wav'
        abs_path = os.path.abspath(file_name)
        myobj.save(abs_path)

        if platform.uname().system == 'Windows':
            try:
                import sounddevice as sd
                import soundfile as sf
            except ImportError:
                pkg_install('sounddevice')
                pkg_install('soundfile')
                import sounddevice as sd
                import soundfile as sf

            data, fs = sf.read(file_name, dtype='float32')
            sd.play(data, fs)
            sd.wait()
        elif platform.uname().system in ['Linux', 'Darwin']:
            if shutil.which('mpg321') is None:
                print_error('mpg321 is not installed on your system.')
                return False
            os.system(f'mpg321 {abs_path}')

        return True
    except Exception as e:
        print_error(e)
        return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='tts_service', help="thing name"
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
    tag_list = [
        MXTag(name='speaker'),
        MXTag(name='tts'),
    ]
    function_list = [
        MXFunction(
            func=speak,
            return_type=MXType.BOOL,
            exec_time=5,
            timeout=60,
            tag_list=tag_list,
            arg_list=[MXArgument(name='text', type=MXType.STRING, bound=(0, 10000))],
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
