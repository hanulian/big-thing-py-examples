from big_thing_py.big_thing import *

import time
import os
import datetime
import subprocess
from glob import glob
from tqdm import tqdm
import cv2

try:
    from picamera2 import Picamera2
except ImportError:
    if is_raspberry_pi():
        os.system('pip3 install picamera2')
        from picamera2 import Picamera2

# 현재 웹캠이 지원하는 해상도 출력
# v4l2-ctl -d /dev/video0 --list-formats-ext


class TimelapseCamera:
    DEFAULT_IMAGE_FOLDER = 'capture_images'
    DEFAULT_VIDEO_FOLDER = 'video_out'
    DEFAULT_CONFIG_PATH = 'config.json'

    def __init__(self, camera_type='usb', width=1280, height=960, cap_num=0, cycle=1000):
        self.camera_type = camera_type
        self.cap = None
        self.width = width
        self.height = height
        self.cap_num = cap_num
        self.vout = None
        self.run_capture = False
        self.cycle = cycle
        self.capture_num = 0

        self.timelapse_event: Event = Event()
        self.timelapse_lock: Lock = Lock()
        self.timelapse_thread: Thread = Thread(target=self.run, daemon=True, args=(self.timelapse_event,))

        if self.camera_type == 'usb':
            self.cap = cv2.VideoCapture(self.cap_num)
            if not self.cap.isOpened():
                for i in range(0, 10):
                    self.cap = cv2.VideoCapture(i)
                    if self.cap.isOpened():
                        print(f'Found /dev/video{i}')
                        break
                else:
                    print('Web cam is not available!')

            supported_resolutions = self.get_supported_resolutions()
            self.set_width(self.width)
            self.set_height(self.height)
        elif self.camera_type == 'picamera':
            self.cap = Picamera2()
            camera_config = self.cap.create_still_configuration(
                main={"size": (self.width, self.height)}, lores={"size": (640, 480)}, display="lores"
            )
            self.cap.configure(camera_config)

    def set_width(self, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def set_height(self, height):
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def make_video(self, src_path=DEFAULT_IMAGE_FOLDER, dst_path=DEFAULT_VIDEO_FOLDER):
        try:
            print(f'Make video start. [video path : {dst_path}]')
            self.run_capture = False

            image_list = glob(f'{src_path}/*.jpg')
            image_list.sort()

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.vout = cv2.VideoWriter(dst_path, fourcc, 30.0, (self.width, self.height))

            for image in tqdm(image_list, desc='image read'):
                frame = cv2.imread(image)
                self.vout.write(frame)
            self.vout.release()
            print(f'Make video finish. [video path : {dst_path}]')

            return True
        except Exception as e:
            print_error(e)
            return False

    def start_capture(self):
        if not self.run_capture:
            self.run_capture = True
        else:
            print('thread already run now')

    def stop_capture(self):
        if self.run_capture:
            self.run_capture = False
        else:
            print('thread already stop now')

    def cap_destroy(self):
        self.cap.release()

    # override of thread class
    def run(self, user_stop_event: Event, folder=DEFAULT_IMAGE_FOLDER):
        print(f'Capture start. [image path : ./{folder}/]')

        prev_millis = 0
        try:
            while not user_stop_event.wait(timeout=0.1):
                if (int(round(time.time() * 1000)) - prev_millis) > self.cycle and self.run_capture:
                    prev_millis = int(round(time.time() * 1000))
                    ret, frame = self.cap.read()
                    if ret:
                        os.makedirs(folder, exist_ok=True)
                        image_name = self.make_image_name(folder)
                        now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        cv2.imwrite(f'{folder}/{image_name}.jpg', frame)
                        print(f'[{now_datetime}] Capture success! [press "v" to make video]\r')
                        self.capture_num += 1
                    else:
                        print('Camera capture failed!')
        except KeyboardInterrupt:
            print('KeyboardInterrupt... end timelapse')
            return False
        except Exception as e:
            print_error(e)
            print('while loop end')

    def run_thread(self):
        self.timelapse_thread.start()

    ##############################################################################################################

    def make_image_name(self, folder: str):
        now = datetime.datetime.now()
        capture_date = now.strftime('%Y%m%d')
        capture_time = now.strftime('%H%M%S')
        # capture_time = now.strftime('%H')

        image_name = '_'.join([capture_date, capture_time])
        image_name_duplicate = glob(f'{folder}/*{image_name}*.jpg')

        if len(image_name_duplicate) > 1:
            tmp_list = []
            for image in image_name_duplicate:
                name_split = image.split('_')
                if len(name_split) > 2:
                    index = image.split('_')[-1][:-4]
                    tmp_list.append(int(index))
            latest_index = max(tmp_list)

            image_name = '_'.join([image_name, str(latest_index + 1)])
        elif len(image_name_duplicate) == 1:
            image_name += '_1'

        return image_name

    def get_supported_resolutions(self) -> List[str]:
        command = f"v4l2-ctl -d {self.cap_num} --list-formats-ext"
        result = subprocess.run(command.split(), stdout=subprocess.PIPE, text=True)
        output = result.stdout
        resolutions = re.findall(r'(\d+)x(\d+)', output)
        return list(set(resolutions))
