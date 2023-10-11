from big_thing_py.utils.common_util import *

PICAMERA = False


try:
    if PICAMERA:
        if not is_raspberry_pi():
            import cv2
        else:
            if check_os_architecture() == '32bit':
                from picamera import PiCamera
            elif check_os_architecture() == '64bit':
                from picamera2 import Picamera2
            else:
                raise Exception('Unknown architecture')
    else:
        import cv2
except ImportError as e:
    install_missing_package(e)


def camera_capture(image_name: str, cam_num: int = 0):
    ret = False

    try:
        if platform.uname().system == 'Darwin':
            cam = cv2.VideoCapture(cam_num)
            curr_time = time.time()
            while time.time() - curr_time < 0.1:
                ret, frame = cam.read()
                cv2.waitKey(30)
                cv2.imwrite(image_name, frame)
        elif platform.uname().system == 'Windows':
            cam = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
            ret, frame = cam.read()
            cv2.imwrite(image_name, frame)
        elif is_raspberry_pi():
            if PICAMERA:
                ret = save_image_from_picamera(filename=image_name)
            else:
                ret = save_image_from_usb_camera(filename=image_name)
        else:
            ret = save_image_from_usb_camera(filename=image_name)
    except:
        return False
    finally:
        if not is_raspberry_pi():
            cam.release()

    return ret


def save_image_from_picamera(filename: str):
    try:
        if check_os_architecture() == '32bit':
            with PiCamera() as camera:
                camera.resolution = camera.MAX_RESOLUTION
                camera.capture(filename)
        elif check_os_architecture() == '64bit':
            camera = Picamera2()
            camera_config = camera.create_still_configuration(main={'size': (1920, 1080)})
            camera.configure(camera_config)
            camera.start()
            camera.capture_file(filename)
            camera.close()
            return True
    except:
        return False


def save_image_from_usb_camera(filename: str):
    try:
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 99999)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 99999)
        ret, frame = cam.read()
        cv2.imwrite(filename, frame)
        cam.release()
        return True
    except:
        return False
