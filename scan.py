# ################################################ #
# #########          SCAN IMAGE          ######### #
# ################################################ #
import os
import random

import cv2
import copy
import imutils
import argparse
from skimage.filters import threshold_local
from pyimagesearch.transform import four_point_transform
from helpers import show_image_normal_window, wait_for_input


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def img_to_grey_gaussian_canny(image):
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    return edged


def find_largest_contours(image):
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts


def close_open_contours(contours):
    cnts = copy.copy(contours)
    # close contours that are open.
    for i, cnt in enumerate(cnts):
        cnts[i] = cv2.convexHull(cnts[i])
    return cnts


def get_n_larger_contours(contours, n):
    return sorted(contours, key=cv2.contourArea, reverse=True)[:n]


def display_contours_on_image(input_output_array, input_array_of_arrays,
                              display_name="", contour_idx=-1,
                              color=(0, 255, 255), thickness=1):
    img = input_output_array.copy()
    cv2.drawContours(input_output_array, input_array_of_arrays, contourIdx=contour_idx,
                     color=color, thickness=thickness)
    show_image_normal_window(display_name, img)
    wait_for_input()
    cv2.destroyAllWindows()


def image_to_black_and_white(image, offset=None, block_size=None):
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if block_size is None or offset is None:
        block_size = 5
        offset = 5
        loop = True
    else:
        loop = False

    while True:
        T = threshold_local(image, block_size=block_size, offset=offset, method="gaussian")
        _wrapped = (image > T).astype("uint8") * 255
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


def scan_image(image, crop_transform=False):
    if crop_transform:

        edged = img_to_grey_gaussian_canny(image)

        cnts = find_largest_contours(edged)

        cnts = close_open_contours(cnts)

        cnts = get_n_larger_contours(cnts, 10)

        areas = list(map(cv2.contourArea, cnts))

        count = 0
        max_area = 0

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        display_contours_on_image(image, [screenCnt], display_name="Outline")

        # apply the four point transform to obtain a top-down
        # view of the original image
        image = four_point_transform(image, screenCnt.reshape(4, 2))

    black_and_white = image_to_black_and_white(image)

    return black_and_white


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-c", "--crop-transform",
                action="store_true",
                default=False,
                help="Crop and transform image searching for document form")

if __name__ == "__main__":
    args = vars(ap.parse_args())

    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    filename_image = args["image"]
    image = cv2.imread(args["image"])
    orig = image.copy()

    scanned = scan_image(orig, args["crop_transform"])

    path_basename, ext = os.path.splitext(filename_image)
    basename = os.path.basename(path_basename)
    dirname = os.path.dirname(path_basename)

    cv2.imwrite(
        dirname + "/" + basename + "_scan_result" + ext,
        scanned)
