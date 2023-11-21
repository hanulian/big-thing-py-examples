from typing import List, Union

from ultralytics import YOLO

# from PIL import Image
# import cv2

from big_thing_py.utils import *

LABEL_MAP = {
    0: 'person',
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    4: 'airplane',
    5: 'bus',
    6: 'train',
    7: 'truck',
    8: 'boat',
    9: 'traffic light',
    10: 'fire hydrant',
    11: 'stop sign',
    12: 'parking meter',
    13: 'bench',
    14: 'bird',
    15: 'cat',
    16: 'dog',
    17: 'horse',
    18: 'sheep',
    19: 'cow',
    20: 'elephant',
    21: 'bear',
    22: 'zebra',
    23: 'giraffe',
    24: 'backpack',
    25: 'umbrella',
    26: 'handbag',
    27: 'tie',
    28: 'suitcase',
    29: 'frisbee',
    30: 'skis',
    31: 'snowboard',
    32: 'sports ball',
    33: 'kite',
    34: 'baseball bat',
    35: 'baseball glove',
    36: 'skateboard',
    37: 'surfboard',
    38: 'tennis racket',
    39: 'bottle',
    40: 'wine glass',
    41: 'cup',
    42: 'fork',
    43: 'knife',
    44: 'spoon',
    45: 'bowl',
    46: 'banana',
    47: 'apple',
    48: 'sandwich',
    49: 'orange',
    50: 'broccoli',
    51: 'carrot',
    52: 'hot dog',
    53: 'pizza',
    54: 'donut',
    55: 'cake',
    56: 'chair',
    57: 'couch',
    58: 'potted plant',
    59: 'bed',
    60: 'dining table',
    61: 'toilet',
    62: 'tv',
    63: 'laptop',
    64: 'mouse',
    65: 'remote',
    66: 'keyboard',
    67: 'cell phone',
    68: 'microwave',
    69: 'oven',
    70: 'toaster',
    71: 'sink',
    72: 'refrigerator',
    73: 'book',
    74: 'clock',
    75: 'vase',
    76: 'scissors',
    77: 'teddy bear',
    78: 'hair drier',
    79: 'toothbrush',
}
INVERTED_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def int_to_label(num: int) -> str:
    return LABEL_MAP[num]


def label_to_int(label: str) -> int:
    return INVERTED_LABEL_MAP[label]


class ObjectDetector:
    def __init__(self, model: str = 'yolov8n.pt', device: str = 'cpu') -> None:
        self._model = YOLO(model)
        self._device = device
        self._predictor = self._model.predict(source=0, stream=True, device=self._device)
        self._predict_thread: MXThread = None

        self.predict_running = False
        # self._model.to('cuda')

        # [
        #     {'label': 'person', 'box': [0.0, 0.0, 0.0, 0.0]},
        # ]
        self.detected_object: List[dict] = None

    def _detect_thread_func(self) -> None:
        # target_label: Union[List[str], str] = 'all'
        # if target_label == 'all' or 'all' in target_label:
        #     target_label_int = list(LABEL_MAP.keys())
        # else:
        #     target_label_int = [
        #         INVERTED_LABEL_MAP[label] for label in target_label if label in INVERTED_LABEL_MAP.keys()
        #     ]
        # results = self._model.predict(source=0, stream=True, classes=target_label_int, device=self._device)
        # results = self._model.predict(source='0', save=True, save_txt=True)
        # results = self._model.predict(source=0, stream=True, device=self._device)

        for result in self._predictor:
            while not self.predict_running:
                time.sleep(THREAD_TIME_OUT * 100)
            # Detection
            result.boxes.xyxy  # box with xyxy format, (N, 4)
            result.boxes.xywh  # box with xywh format, (N, 4)
            result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
            result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
            result.boxes.conf  # confidence score, (N, 1)
            result.boxes.cls  # cls, (N, 1)

            # Segmentation
            # result.masks.data  # masks, (N, H, W)
            # result.masks.xy  # x,y segments (pixels), List[segment] * N
            # result.masks.xyn  # x,y segments (normalized), List[segment] * N

            # Classification
            result.probs  # cls prob, (num_class, )

            self.detected_object = []
            for obj in result.boxes:
                xyxy = obj.xyxy.tolist()
                # xywh = obj.xywh.tolist()
                # xyxyn = obj.xyxyn.tolist()
                # xywhn = obj.xywhn.tolist()
                # conf = obj.conf

                self.detected_object.append(
                    {
                        'label': int_to_label(int(obj.cls)),
                        'box': xyxy,
                    }
                )

    def detect_start(self) -> bool:
        if not self._predict_thread:
            self._predict_thread = MXThread(target=self._detect_thread_func)
            self.predict_running = True
            self._predict_thread.start()

        if self._predict_thread.is_alive():
            self.predict_running = True
        else:
            self.predict_running = True

        return self.predict_running

    def detect_stop(self) -> None:
        self.predict_running = False


if __name__ == '__main__':
    detector = ObjectDetector()
    detector.detect_start(['person'])
    # print(detector.detected_object)
