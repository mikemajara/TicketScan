# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages

import os
import cv2
import random
import imutils
import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.filters import threshold_local
from pyimagesearch.transform import four_point_transform


DEBUG = False
PATH_WORKDIR = os.getcwd()
PATH_IMAGES = 'images'  # os.path.join(PATH_WORKDIR, "images")
# FILENAME_IMAGE = 'merc3.jpeg'

BGR_BLUE = (255, 0, 0)
BGR_GREEN = (0, 192, 0)
BGR_RED = (0, 0, 255)
BGR_PINK = (208, 96, 255)
BGR_PURPLE = (255, 32, 160)
BGR_YELLOW_GREEN = (128, 255, 96)
BGR_YELLOW = (32, 224, 225)

BGR_UPPER = [BGR_RED, BGR_PURPLE]
BGR_LOWER = [BGR_GREEN, BGR_YELLOW]

KEY_PLUS = 43
KEY_MINUS = 45
KEY_RIGHT_ACCENT = 96
KEY_DOT = 46
KEY_ENTER = 13
KEY_ESC = 27


def wait_for_input():
    if DEBUG:
        return cv2.waitKeyEx(0)
    else:
        return KEY_ENTER


def wait_for_input_no_matter_what():
    return cv2.waitKeyEx(0)


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


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
    cv2.setWindowProperty(img_title, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(img_title, image)


def threshold_image(wrapped, offset=None, block_size=None):
    if block_size is None or offset is None:
        block_size = 5
        offset = 5
        loop = True
    else:
        loop = False

    while True:
        T = threshold_local(wrapped, block_size=block_size, offset=offset, method="gaussian")
        _wrapped = (wrapped > T).astype("uint8") * 255
        img_title = "Thresholded image"  # block_size=" + str(block_size) + " offset=" + str(offset)
        print("Th image\n  offset=" + str(offset) + " block_size=" + str(block_size))

        show_image_normal_window(img_title, _wrapped)
        key = wait_for_input()

        print("key pressed: " + str(key))
        if key == 43:  # +
            block_size += 2
        elif key == 45:  # -
            block_size -= 2
        elif key == 96:  # `
            offset -= 1
        elif key == 46:  # .
            offset += 1
        elif key == 27 or key == 13 or loop == False:  # ESC or ENTER or values already defined
            break

    cv2.destroyAllWindows()
    return _wrapped


def get_weighted_array(length, margin_threshold=.04):
    margin = round(length * margin_threshold)
    jump = 1 / margin
    array = np.ones(length)

    pre = np.arange(0, 1, jump)
    post = pre[::-1]

    array[0:margin] = pre
    array[length - margin:] = post

    return array


def generate_motion_kernel(size=15):
    # generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size
    return kernel_motion_blur


def generate_motion_kernel_vertical(size=15):
    # generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[:, int((size-1)/2)] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size
    return kernel_motion_blur


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
filename_image = args["image"]
image = cv2.imread(args["image"])
orig = image.copy()
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# ################################################# #
# #########     SLICE IMAGE IN PIECES     ######### #
# ################################################# #


show_image_normal_window("Scanned", img)
wait_for_input()
cv2.destroyAllWindows()

# (2) threshold
threshold_pxl_density, threshed = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

show_image_normal_window("Thresholded image", img)
key = wait_for_input()
cv2.destroyAllWindows()

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
cv2.destroyAllWindows()

# (5) find and draw the upper and lower boundary of each lines
threshold_pxl_density = 5.5

# TODO Extract method
# uppers, lowers, img = draw_cut_lines(original, rotated, th)
hist1 = []

kernel_horiz = generate_motion_kernel(100)
# kernel_vert = generate_motion_kernel_vertical(5)
blurred = cv2.filter2D(rotated, -1, kernel_horiz)
# blurred = cv2.filter2D(blurred, -1, kernel_vert)

threshold_pxl_line = 7
while True:

    H, W = img.shape[:2]

    hist2d = cv2.reduce(blurred, 1, cv2.REDUCE_AVG)
    hist = hist2d.reshape(-1)

    _rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
    _blurred = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

    # th += .5
    # Old algorithm
    uppers = [y - 1 for y in range(H - 1) if hist[y] <= threshold_pxl_density and hist[y + 1] > threshold_pxl_density]
    lowers = [y + 1 for y in range(H - 1) if hist[y] > threshold_pxl_density and hist[y + 1] <= threshold_pxl_density]

    color_count = 0
    for y in uppers:
        pt_y = max(y - threshold_pxl_line, 0)
        cv2.line(_rotated, (0, pt_y), (W, pt_y), BGR_UPPER[color_count % 2], 1, cv2.LINE_8)
        # cv2.line(_blurred, (0, y), (W, y), (0, 0, 255), 1, cv2.LINE_8)
        color_count += 1

    color_count = 0
    for y in lowers:
        pt_y = min(y + threshold_pxl_line, H)
        cv2.line(_rotated, (0, pt_y), (W, pt_y), BGR_LOWER[color_count % 2], 1, cv2.LINE_8)
        # cv2.line(_blurred, (0, y), (W, y), (0, 255, 0), 1, cv2.LINE_8)
        color_count += 1

    print("Result for threshold_pxl_density: " + str(threshold_pxl_density))
    print("Result for threshold_pxl_line: " + str(threshold_pxl_line) + "\n")
    show_image_normal_window("Lines result", _rotated)
    key = wait_for_input()

    print("key pressed: " + str(key))
    if key == KEY_PLUS:
        threshold_pxl_density += .5
    elif key == KEY_MINUS:
        threshold_pxl_density -= .5
    elif key == KEY_RIGHT_ACCENT:
        threshold_pxl_line += 1
    elif key == KEY_DOT:
        threshold_pxl_line -= 1
    elif key == KEY_ENTER or key == KEY_ESC:
        break


cv2.destroyAllWindows()

# im_path = "path/to/image"
# img = cv2.imread(im_path)

# #### (6) Crop and write images to output #### #
                                                                                                            
threshold_pxl_cut = 0
parameters = str(threshold_pxl_density) + "_" + str(threshold_pxl_line) + "_" + str(threshold_pxl_cut)

orig_img = cv2.imread(get_image_path(filename_image))

no_ext_filename, ext = os.path.splitext(filename_image)
os.makedirs(
    'output/cropped/' + no_ext_filename + "_" + parameters,
    exist_ok=True
)

if len(lowers) != len(uppers):
    if lowers[0] < uppers[0]:
        lowers = lowers[1:]
    else:
        uppers = uppers[:-1]

line_mean_hight = np.mean(np.array(list(map(lambda x: x[0] - x[1], zip(lowers, uppers)))))
threshold_pxl_cut = line_mean_hight / 2

for lower, upper in zip(lowers, uppers):

    if lower-upper > line_mean_hight / 2 and lower-upper < line_mean_hight * 2:

        pt_upper = max(upper - threshold_pxl_line, 0)
        pt_lower = min(lower + threshold_pxl_line, H)

        crop_img = img[pt_upper:pt_lower, 0:W]
        fname = "croped_" + str(lower) + "_" + str(upper) + ".png"
        cv2.imwrite("output/cropped/" + no_ext_filename + "_" + parameters + "/" + fname, crop_img)

cv2.imwrite("output/cropped/" + no_ext_filename + "_" + parameters + "/img" + ext, img)


# wait_for_input()
print("Done!")
# res_img = Image.open("result" + str(i) + ".png")
# res_img.show()
