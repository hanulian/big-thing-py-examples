import random
import os
import cv2
import time
import darknet.darknet as darknet
import argparse
from queue import Queue

from big_thing_py.big_thing import *

detections_pick = None
detected_object_window = {}


def arg_parse():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")

    parser.add_argument(
        "--name", '-n', action='store', type=str, required=False, default='object_detector_big_thing', help="thing name"
    )
    parser.add_argument(
        "--host", '-ip', action='store', type=str, required=False, default='127.0.0.1', help="host name"
    )
    parser.add_argument("--port", '-p', action='store', type=int, required=False, default=1883, help="port")
    parser.add_argument(
        "--alive_cycle", '-ac', action='store', type=int, required=False, default=60, help="alive cycle"
    )
    parser.add_argument("--log", action='store_true', dest='log', required=False, default=True, help="log enable")

    parser.add_argument("--input", type=str, default=0, help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="", help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default="darknet/yolov4-csp.weights", help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true', help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true', help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default="darknet/cfg/yolov4-csp.cfg", help="path to config file")
    parser.add_argument("--data_file", default="darknet/cfg/coco.data", help="path to data file")
    parser.add_argument("--thresh", type=float, default=0.25, help="remove detections with confidence below this value")
    return parser.parse_args()


def str2int(video_path):
    """
    argparse returns and string althout webcam uses int (0, 1 ...)
    Cast to int if needed
    """
    try:
        return int(video_path)
    except ValueError:
        return video_path


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise (ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise (ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise (ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if str2int(args.input) == str and not os.path.exists(args.input):
        raise (ValueError("Invalid video path {}".format(os.path.abspath(args.input))))


def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


def convert2relative(bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h = bbox
    _height = darknet_height
    _width = darknet_width
    return x / _width, y / _height, w / _width, h / _height


def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x = int(x * image_w)
    orig_y = int(y * image_h)
    orig_width = int(w * image_w)
    orig_height = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


def convert4cropping(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_left = int((x - w / 2.0) * image_w)
    orig_right = int((x + w / 2.0) * image_w)
    orig_top = int((y - h / 2.0) * image_h)
    orig_bottom = int((y + h / 2.0) * image_h)

    if orig_left < 0:
        orig_left = 0
    if orig_right > image_w - 1:
        orig_right = image_w - 1
    if orig_top < 0:
        orig_top = 0
    if orig_bottom > image_h - 1:
        orig_bottom = image_h - 1

    bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

    return bbox_cropping


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height), interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)
        detections_queue.put(detections)
        fps = int(1 / (time.time() - prev_time))
        fps_queue.put(fps)
        print("FPS: {}".format(fps))
        darknet.print_detections(detections, args.ext_output)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, fps_queue):
    global detections_pick

    random.seed(3)  # deterministic bbox colors
    video = set_saved_video(cap, args.out_filename, (video_width, video_height))
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        detections_pick = detections

        update_detection_window()

        fps = fps_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            if not args.dont_show:
                cv2.imshow('Inference', image)
            if args.out_filename is not None:
                video.write(image)
            if cv2.waitKey(fps) == 27:
                break
    cap.release()
    video.release()
    cv2.destroyAllWindows()


def update_detection_window():
    global detected_object_window
    global detections_pick

    for label in detected_object_window:
        detected_object_window[label] = detected_object_window[label][1:] + [None]

    for detection in detections_pick:
        new_detected_object = {
            'label': detection[0],
            'confidence': detection[1],
            'x': detection[2][0],
            'y': detection[2][1],
            'w': detection[2][2],
            'h': detection[2][3],
            'updated': False,
        }
        label = new_detected_object['label']

        if not label in detected_object_window:
            detected_object_window[label] = [None for i in range(5)]
        detected_object_window[label][-1] = new_detected_object


def get_object_info(target_label: str) -> bool:
    global detected_object_window

    object_sum = 0

    if target_label in detected_object_window:
        for detected_object in detected_object_window[target_label]:
            if not detected_object == None:
                object_sum += 1
        if object_sum > 0:
            return True
        else:
            return False
    else:
        return False


def init_darknet(args):
    # darknet init
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    check_arguments_errors(args)
    network, class_names, class_colors = darknet.load_network(
        args.config_file, args.data_file, args.weights, batch_size=1
    )

    darknet_width = darknet.network_width(network)
    darknet_height = darknet.network_height(network)
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    Thread(target=video_capture, daemon=True, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, daemon=True, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, daemon=True, args=(frame_queue, detections_queue, fps_queue)).start()


def generate_thing(args):
    tags = [
        MXTag(name='object_detector'),
    ]
    argments = [
        MXArgument(name='target_label', type='string', bound=(0, 100)),
    ]

    value_list = []
    function_list = [
        MXFunction(name='get_object_info', func=get_object_info, return_type='bool', tag_list=tags, arg_list=argments)
    ]
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
    init_darknet(args)
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()
