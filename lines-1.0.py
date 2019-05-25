#!/usr/bin/python3
# 2018.01.16 01:11:49 CST
# 2018.01.16 01:55:01 CST
import cv2
import os

import imutils
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

PATH_WORKDIR = os.getcwd()
PATH_IMAGES = 'images'  # os.path.join(PATH_WORKDIR, "images")
FILENAME_IMAGE = 'contour_result_no_threshold.jpg'

DEBUG = True


def wait_for_input():
    if DEBUG:
        return cv2.waitKey(0)


def fig(width, height):
    plt.figure(figsize=(width, height))


def get_image_path(name: str):
    return os.path.join(PATH_IMAGES, name)


def read_image(file_name):
    return cv2.imread(file_name)


def plot_image(image, size_x=10, size_y=10):
    fig(size_x, size_y)
    plt.imshow(image)


def show_image_normal_window(img_title, image, height=None, width=None):
    if height is None or width is None:
        height = image.shape[1]
        width = image.shape[0]

    cv2.namedWindow(img_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(img_title, height, width)
    cv2.imshow(img_title, image)


# How to show images
# img2 = Image.open(get_image_path(FILENAME_IMAGE))
# img2.show()

# img = read_image(get_image_path(FILENAME_IMAGE))
# plot_image(img, 5, 5)


'''
# (1) read
'''
img = cv2.imread(get_image_path(FILENAME_IMAGE))
# ratio = img.shape[0] / 500.0
# orig = img.copy()
# img = imutils.resize(img, height=500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


show_image_normal_window("Gray image", gray)
key = wait_for_input()

# (2) threshold
th, threshed = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

show_image_normal_window("Thresholded image", gray)
key = wait_for_input()

# (3) minAreaRect on the nozeros
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx, cy), (w, h), ang = ret
if w > h:
    w, h = h, w
    ang += 90

# (4) Find rotated matrix, do rotation
M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

show_image_normal_window("Rotated image", rotated)
key = wait_for_input()

# (5) find and draw the upper and lower boundary of each lines
th = 2

# for i in range(20):
while True:
    hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)

    # th += .5
    H, W = img.shape[:2]
    uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
    lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]

    _rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
    for y in uppers:
        cv2.line(_rotated, (0, y), (W, y), (255, 0, 0), 1)

    for y in lowers:
        cv2.line(_rotated, (0, y), (W, y), (0, 255, 0), 1)

    cv2.imwrite("output/result.png", _rotated)

    show_image_normal_window(_rotated, "Result for th: " + str(th))
    key = wait_for_input()

    print(key)
    if key == 43:  # Left
        th += .5
    elif key == 45:  # Right
        th -= .5
    elif key == 27:
        break
    cv2.destroyAllWindows()

# im_path = "path/to/image"
# img = cv2.imread(im_path)

# #### (6) Crop and write images to output #### #

# orig_img = cv2.imread(get_image_path(FILENAME_IMAGE))
#
# no_ext_filename = os.path.splitext(FILENAME_IMAGE)[0]
# os.makedirs(
#     'output/cropped/' + no_ext_filename,
#     exist_ok=True
# )
#
# for lower, upper in zip(lowers + [H], [0] + uppers):
#
#     if abs(upper-lower) > 5:
#         crop_img = orig_img[upper:lower, 0:W]
#         fname = "croped_" + str(lower) + "_" + str(upper) + ".png"
#         cv2.imwrite("output/cropped/" + no_ext_filename + "/" + fname, crop_img)


# wait_for_input()
print("Done!")
# res_img = Image.open("result" + str(i) + ".png")
# res_img.show()

