import argparse
from collections import Counter

from big_thing_py.big_thing import *
from object_detector_utils import *


object_detector = ObjectDetector()


def detect_start() -> bool:
    global object_detector

    return object_detector.detect_start()


def detect_stop() -> bool:
    global object_detector

    object_detector.detect_stop()

    return True


def get_detected_object() -> str:
    global object_detector

    if object_detector.detected_object is None:
        return ''

    labels = [item['label'] for item in object_detector.detected_object]
    label_counts = dict(Counter(labels))
    object_info_str = ' '.join([f'{label}:{count}' for label, count in label_counts.items()])

    return object_info_str


def person_num() -> int:
    person_num = 0
    detected_object = get_detected_object()

    object_list = detected_object.split(' ')
    for object in object_list:
        if 'person' in object:
            person_num = int(object.split(':')[1])
            break

    return person_num


def is_detection_running() -> bool:
    global object_detector

    return (object_detector.detected_object is not None) and object_detector.predict_running


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name', '-n', action='store', type=str, required=False, default='object_detector_big_thing', help='thing name'
    )
    parser.add_argument(
        '--host', '-ip', action='store', type=str, required=False, default='127.0.0.1', help='host name'
    )
    parser.add_argument('--port', '-p', action='store', type=int, required=False, default=1883, help='port')
    parser.add_argument(
        '--alive_cycle', '-ac', action='store', type=int, required=False, default=60, help='alive cycle'
    )
    parser.add_argument('--auto_scan', '-as', action='store_true', required=False, help='middleware auto scan enable')
    parser.add_argument('--log', action='store_true', required=False, help='log enable')
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
        MXTag(name='object_detector'),
        MXTag(name='big_thing'),
    ]
    value_list = [
        MXValue(
            name='detected_object',
            func=get_detected_object,
            type=MXType.STRING,
            bound=(0, 10000),
            tag_list=tag_list,
            cycle=1,
        ),
        MXValue(
            name='is_detection_running',
            func=is_detection_running,
            type=MXType.BOOL,
            bound=(0, 10000),
            tag_list=tag_list,
            cycle=1,
        ),
        MXValue(
            name='person_num',
            func=person_num,
            type=MXType.INTEGER,
            bound=(0, 10000),
            tag_list=tag_list,
            cycle=1,
        ),
    ]
    function_list = [
        MXFunction(
            name='detect_start',
            func=detect_start,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
        MXFunction(
            name='detect_stop',
            func=detect_stop,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
        ),
    ]

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
