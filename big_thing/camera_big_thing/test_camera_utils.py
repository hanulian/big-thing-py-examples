import os
import cv2
from camera_utils import save_image_from_picamera, save_image_from_usb_camera


def test_save_image_from_usb_camera():
    try:
        os.remove('test_usb.jpg')
    except:
        pass

    assert save_image_from_usb_camera(filename='test_usb.jpg') == True
    assert os.path.exists('test_usb.jpg')


def test_save_image_from_picamera():
    try:
        os.remove('test_picamera.jpg')
    except:
        pass

    assert save_image_from_picamera(filename='test_picamera.jpg') == True
    assert os.path.exists('test_picamera.jpg')
