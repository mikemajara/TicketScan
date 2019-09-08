import os
import sys
import cv2
import logging

KEY_PLUS = 43
KEY_MINUS = 45
KEY_RIGHT_ACCENT = 96
KEY_DOT = 46
KEY_ENTER = 13
KEY_ESC = 27


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def wait_for_input():
    return cv2.waitKeyEx(0)


def wait_for_input_no_matter_what():
    return cv2.waitKeyEx(0)


def show_image_normal_window(img_title, image, height=None, width=None):
    if height is None or width is None:
        height = image.shape[1]
        width = image.shape[0]

    cv2.namedWindow(img_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(img_title, height, width)
    cv2.setWindowProperty(
        img_title, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(img_title, image)


def get_path_base_and_ext(filename_image):
    path_basename, ext = os.path.splitext(filename_image)
    basename = os.path.basename(path_basename)
    path = os.path.dirname(path_basename)
    return path, basename, ext
