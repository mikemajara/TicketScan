import os
import cv2
import argparse
import numpy as np
from datetime import datetime
from .helpers import show_image_normal_window, wait_for_input, get_path_base_and_ext


PATH_WORKDIR = os.getcwd()
PATH_IMAGES = 'images'

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

DEFAULT_THRESHOLD_PIXEL_DENSITY = 5.5
DEFAULT_LINE_PADDING = 7


def get_image_path(name: str):
    return os.path.join(PATH_IMAGES, name)


def get_inverted_thresholded_image(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)


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


def get_blurred_image(image, kernel_size=15):
    kernel_horiz = generate_motion_kernel(kernel_size)
    return cv2.filter2D(image, -1, kernel_horiz)


def pair_lower_upper_bounds(lowers, uppers):
    if len(lowers) != len(uppers):
        if lowers[0] < uppers[0]:
            return lowers[1:], uppers
        else:
            return lowers, uppers[:-1]
    return lowers, uppers


def slice(path_image, interactive=False, threshold_pxl_density=5.5, line_padding=7):

    filename_image = path_image
    image = cv2.imread(path_image)

    orig = image.copy()
    working_image = image.copy()

    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2GRAY)

    computed_threshold, working_image = get_inverted_thresholded_image(
        working_image)

    blurred = get_blurred_image(image=working_image, kernel_size=100)

    while True:

        H, W = working_image.shape[:2]

        # (miguel) Obtain reduced 1-dimension array of average
        # of pixels to check the density of ink on lines
        hist2d = cv2.reduce(blurred, 1, cv2.REDUCE_AVG)
        hist = hist2d.reshape(-1)

        uppers = [
            y - 1 for y in range(H - 1) if hist[y] <= threshold_pxl_density < hist[y + 1]]
        lowers = [
            y + 1 for y in range(H - 1) if hist[y] > threshold_pxl_density >= hist[y + 1]]

        # (miguel) change again to color so we can appreciate
        # the lines we will draw on the image
        display_image = working_image.copy()
        display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2BGR)

        color_count = 0
        for y in uppers:
            pt_y = max(y - line_padding, 0)
            cv2.line(display_image, (0, pt_y), (W, pt_y),
                     BGR_UPPER[color_count % 2], 1, cv2.LINE_8)
            color_count += 1

        color_count = 0
        for y in lowers:
            pt_y = min(y + line_padding, H)
            cv2.line(display_image, (0, pt_y), (W, pt_y),
                     BGR_LOWER[color_count % 2], 1, cv2.LINE_8)
            color_count += 1

        if interactive:
            print("Result for threshold_pxl_density: " +
                  str(threshold_pxl_density))
            print("Result for threshold_pxl_line: " + str(line_padding) + "\n")
            show_image_normal_window("Lines result", display_image)
            key = wait_for_input()

            print("key pressed: " + str(key))
            if key == KEY_PLUS:
                threshold_pxl_density += .5
            elif key == KEY_MINUS:
                threshold_pxl_density -= .5
            elif key == KEY_RIGHT_ACCENT:
                line_padding += 1
            elif key == KEY_DOT:
                line_padding -= 1
            elif key == KEY_ENTER or key == KEY_ESC:
                break
        else:
            break

    cv2.destroyAllWindows()

    # #### (6) Crop and write images to output #### #
    lowers, uppers = pair_lower_upper_bounds(lowers, uppers)
    line_mean_hight = np.mean(
        np.array(list(map(lambda x: x[0] - x[1], zip(lowers, uppers)))))

    lower_th_pxl_cut = line_mean_hight / 2
    upper_th_pxl_cut = line_mean_hight * 2

    parameters_str = str(threshold_pxl_density) + "_" + \
        str(line_padding)  # + "_" + str(threshold_pxl_cut)
    path, basename, ext = get_path_base_and_ext(filename_image)
    path_output = path + '/output_cropped/' + basename + "_" + parameters_str
    os.makedirs(path_output, exist_ok=True)

    for lower, upper in zip(lowers, uppers):
        if lower_th_pxl_cut < lower - upper < upper_th_pxl_cut:
            pt_upper = max(upper - line_padding, 0)
            pt_lower = min(lower + line_padding, H)

            crop_img = orig[pt_upper:pt_lower, 0:W]
            fname = "cropped_" + str(lower) + "_" + str(upper) + ".png"
            cv2.imwrite(path_output + "/" + fname, crop_img)

    now_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    cv2.imwrite(path_output + "/original_" + now_timestamp + ext, orig)

    return path_output


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-d", "--threshold-pxl-density",
                type=float,
                default=DEFAULT_THRESHOLD_PIXEL_DENSITY,
                help="Path to the image to be scanned")
ap.add_argument("-p", "--line-padding",
                default=DEFAULT_LINE_PADDING,
                type=int,
                help="Path to the image to be scanned")
ap.add_argument("-v", "--interactive",
                action="store_true",
                default=False,
                help="Slice interactively showing image to modify variables with [ ` . + - ] characters")


if __name__ == "__main__":
    args = vars(ap.parse_args())

    slice(path_image=args["image"],
          interactive=args["interactive"],
          threshold_pxl_density=args["threshold_pxl_density"],
          line_padding=args["line_padding"]
          )
