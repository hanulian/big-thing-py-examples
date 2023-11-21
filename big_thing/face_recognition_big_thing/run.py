from big_thing_py.big_thing import *
from face_recognition_utils import FaceRecognizer

import argparse
from func_timeout import func_timeout, FunctionTimedOut
import cv2


face_recognition_client = FaceRecognizer(dataset_path='dataset', model_path='model.clf')


def add_face() -> bool:
    global face_recognition_client

    try:
        face_recognition_client.add_face()
        return True
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'add_face failed...')
        return False


def delete_face(name: str) -> bool:
    global face_recognition_client

    try:
        face_recognition_client.delete_face(name)
        return True
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'delete_face {name} failed...')
        return False


def detect_face() -> str:
    global face_recognition_client

    try:
        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            face_location = face_recognition_client.detect_face(frame)
            for top, right, bottom, left in face_location:
                cropped_img = frame[top:bottom, left:right]
                cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                output_image_path = f'detected_face.jpg'
                cv2.imwrite(output_image_path, cropped_img_rgb)
                return os.path.abspath(output_image_path)
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'detect_face failed...')
        return False
    finally:
        cam.release()


def face_recognition(timeout: float) -> str:
    global face_recognition_client

    def wrapper():
        try:
            cam = cv2.VideoCapture(0)
            while True:
                ret, frame = cam.read()
                if not ret:
                    continue

                face_location = face_recognition_client.detect_face(frame)
                for top, right, bottom, left in face_location:
                    cropped_img = frame[top:bottom, left:right]
                    cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
                    result = face_recognition_client.recognize_from_frame(cropped_img_rgb)
                    person = face_recognition_client.result_to_person(result)
                    return person
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'face_recognition failed...')
            return ''
        finally:
            cam.release()

    try:
        return func_timeout(timeout, wrapper)
    except FunctionTimedOut:
        MXLOG_DEBUG(f'face_recognition timeout {timeout}...')
        return ''


def face_recognition_from_file(img_path: str) -> str:
    global face_recognition_client

    try:
        result = face_recognition_client.recognize(img_path)
        person = face_recognition_client.result_to_person(result)
        return person
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'face_recognition failed...')
        return ''


def check_in(person: str) -> bool:
    global face_recognition_client

    try:
        with open('attendance_log.txt', 'a') as f:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{current_time}] {person} check in.\n")
        return True
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'check_in failed...')
        return False


def check_out(person: str) -> bool:
    global face_recognition_client

    try:
        with open('attendance_log.txt', 'a') as f:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{current_time}] {person} check out.\n")
        return True
    except Exception as e:
        print_error(e)
        MXLOG_DEBUG(f'check_out failed...')
        return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name',
        '-n',
        action='store',
        type=str,
        required=False,
        default='face_recognition_big_thing',
        help='thing name',
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
        '--log_mode', action='store', type=str, required=False, default=MXPrintMode.ABBR.value, help='log mode'
    )
    parser.add_argument(
        '--append_mac',
        '-am',
        action='store_true',  # store_true, store_false
        required=False,
        help='append mac address to thing name',
    )
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [
        MXTag(name='face'),
        MXTag(name='big_thing'),
    ]

    function_list = [
        MXFunction(
            func=add_face,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[],
            energy=45,
        ),
        MXFunction(
            func=delete_face,
            return_type=MXType.BOOL,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='name',
                    type=MXType.STRING,
                    bound=(0, 10000),
                )
            ],
            energy=12,
        ),
        MXFunction(
            func=detect_face,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[],
            energy=12,
        ),
        MXFunction(
            func=face_recognition,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='timeout',
                    type=MXType.DOUBLE,
                    bound=(0, 10000),
                )
            ],
            energy=12,
        ),
        MXFunction(
            func=face_recognition_from_file,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='img_path',
                    type=MXType.STRING,
                    bound=(0, 10000),
                ),
            ],
            energy=12,
        ),
        MXFunction(
            func=check_in,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='person',
                    type=MXType.STRING,
                    bound=(0, 10000),
                ),
            ],
            energy=12,
        ),
        MXFunction(
            func=check_out,
            return_type=MXType.STRING,
            tag_list=tag_list,
            arg_list=[
                MXArgument(
                    name='person',
                    type=MXType.STRING,
                    bound=(0, 10000),
                ),
            ],
            energy=12,
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
