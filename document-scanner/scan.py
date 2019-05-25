# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
import random

from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

DEBUG = True


def wait_for_input():
    if DEBUG:
        return cv2.waitKeyEx(0)


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def show_image_normal_window(image, img_title, height=None, width=None):
    if height is None or width is None:
        height = image.shape[1]
        width = image.shape[0]

    cv2.namedWindow(img_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(img_title, height, width*2)
    cv2.setWindowProperty(img_title, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(img_title, image)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
# ratio = image.shape[0] / 500.0
orig = image.copy()
# image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
# wait_for_input()
# cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for i, cnt in enumerate(cnts):
    cnts[i] = cv2.convexHull(cnts[i])

cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
areas = list(map(cv2.contourArea, cnts))


# for c in cnts:
#     print(cv2.arcLength(c, True))
#     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
#     cv2.imshow("Outline", image)
#     wait_for_input()
#     cv2.destroyAllWindows()


count = 0
max_area = 0
# loop over the contours
for c in cnts:
    # approximate the contour

    perimetre = cv2.arcLength(c, True)
    area = cv2.contourArea(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimetre, True)

    # cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    # cv2.imshow("Contour" + str(count), image)
    # wait_for_input()
    # cv2.destroyAllWindows()
    # count += 1

    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if 3 < len(approx) < 6 and area > max_area:
        epsylon = 0.02
        while len(approx) > 4:
            approx = cv2.approxPolyDP(c, epsylon, True)
            epsylon += 0.1
            count += 1

        cv2.drawContours(image, [approx], -1, random_color(), 2)
        cv2.imshow("Contour" + str(count) + " " + str(len(approx)) + " sides ", image)
        wait_for_input()
        cv2.destroyAllWindows()
        count += 1

        screenCnt = approx
        max_area = area

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 255), 1)
cv2.imshow("Outline", image)
wait_for_input()


# apply the four point transform to obtain a top-down
# view of the original image
wrapped = four_point_transform(orig, screenCnt.reshape(4, 2))
cv2.imshow("apply the four point transform...", wrapped)
wait_for_input()

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
wrapped = cv2.cvtColor(wrapped, cv2.COLOR_BGR2GRAY)
cv2.imshow("convert the warped image to grayscale...", wrapped )
wait_for_input()

cv2.imwrite("output/contour_result_no_threshold.jpg", wrapped)

# for block_size in list(range(4, 20))[1::2]:
#     for offset in range(5, 15):
block_size = 5
offset = 5
while True:
    T = threshold_local(wrapped, block_size=block_size, offset=offset, method="gaussian")
    _wrapped = (wrapped > T).astype("uint8") * 255
    img_title = "Thresholded image"  # block_size=" + str(block_size) + " offset=" + str(offset)
    print("Thresholded image offset=" + str(offset) + " block_size=" + str(block_size))

    show_image_normal_window(_wrapped, img_title)
    key = wait_for_input()

    print(key)
    if key == 43:  # +
        block_size += 2
    elif key == 45:  # -
        block_size -= 2
    elif key == 96:  # `
        offset -= 1
    elif key == 46:  # .
        offset += 1
    elif key == 27:  # ESC
        break

    # cv2.destroyAllWindows()

T = threshold_local(wrapped, 11, offset=10, method="gaussian")
wrapped = (wrapped > T).astype("uint8") * 255
cv2.imshow("convert the warped image to grayscale...", wrapped)
wait_for_input()


# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(wrapped, height=650))
cv2.imwrite("output/contour_result.jpg", wrapped)
wait_for_input()
