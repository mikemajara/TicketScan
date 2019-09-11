import os
# import cv2
import logging
import argparse
import numpy as np
from datetime import datetime
from helpers import show_image_normal_window, wait_for_input, get_path_base_and_ext, setup_logging

try:
    from cv2 import cv2
except ImportError:
    pass

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

DEFAULT_TH_PIXEL_DENSITY = 5.5
DEFAULT_LINE_PADDING = 7
DEFAULT_KERNEL_SIZE = 100
DEFAULT_CUT_MARGIN_FACTOR = 0.5

logger = logging.getLogger(__name__)

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


def pair_upper_lower_bounds(uppers, lowers):
    if len(uppers) != len(lowers):
        # an upper border should not have
        # a higher value than a lower border
        # (in images [0,0] is the top left corner)
        if uppers[0] > lowers[0]:
            return uppers, lowers[1:]
        else:
            return uppers[:-1], lowers
    return uppers, lowers


def get_image_cropped(img, upper_bound, lower_bound):
    H, W = img.shape[:2]

    return img.copy()[upper_bound:lower_bound, 0:W]


def draw_slices_on_image(img, uppers, lowers, line_padding=DEFAULT_LINE_PADDING, num_colors=1):
    display_image = img.copy()

    H, W = img.shape[:2]

    color_idx = 0
    for y in uppers:
        pt_y = max(y - line_padding, 0)
        cv2.line(display_image, (0, pt_y), (W, pt_y),
                 BGR_UPPER[color_idx], 1, cv2.LINE_8)
        color_idx = (color_idx + 1) % num_colors

    color_idx = 0
    for y in lowers:
        pt_y = min(y + line_padding, H)
        cv2.line(display_image, (0, pt_y), (W, pt_y),
                 BGR_LOWER[color_idx], 1, cv2.LINE_8)
        color_idx = (color_idx + 1) % num_colors

    return display_image


def get_slices(image,
               th_pxl_density=DEFAULT_TH_PIXEL_DENSITY,
               kernel_size=DEFAULT_KERNEL_SIZE):
    working_image = image.copy()

    blurred = get_blurred_image(image=working_image, kernel_size=kernel_size)

    H, W = working_image.shape[:2]

    # (miguel) Obtain reduced 1-dimension array of average
    # of pixels to check the density of ink on lines
    hist2d = cv2.reduce(blurred, 1, cv2.REDUCE_AVG)
    hist = hist2d.reshape(-1)

    uppers = [
        y - 1 for y in range(H - 1) if hist[y] <= th_pxl_density < hist[y + 1]]
    lowers = [
        y + 1 for y in range(H - 1) if hist[y] > th_pxl_density >= hist[y + 1]]

    return uppers, lowers


def handle_interactive_key_input(th_pxl_density, line_padding):
    flag_interactive = True

    key = wait_for_input()

    logger.info("key pressed: " + str(key))

    if key == KEY_PLUS:
        th_pxl_density += .5
    elif key == KEY_MINUS:
        th_pxl_density -= .5
    elif key == KEY_RIGHT_ACCENT:
        line_padding += 1
    elif key == KEY_DOT:
        line_padding -= 1
    elif key == KEY_ENTER or key == KEY_ESC:
        flag_interactive = False

    return th_pxl_density, line_padding, flag_interactive


def get_line_mean_hight(uppers, lowers):
    return np.mean(
        np.array(list(map(lambda x: x[1] - x[0], zip(uppers, lowers))))
    )


def is_height_cut_margin_valid(x, average, margin_factor=0.5):
    # valid height = average +/- (average * factor)
    return abs(average - x) < average * margin_factor


def get_slices_as_img_list(img, upper_bounds, lower_bounds, line_padding, margin_factor):
    slices = []

    H, W = img.shape[:2]

    line_mean_hight = get_line_mean_hight(upper_bounds, lower_bounds)

    for upper, lower in zip(upper_bounds, lower_bounds):
        slice_height = lower - upper

        if is_height_cut_margin_valid(slice_height, line_mean_hight, margin_factor=margin_factor):
            pt_upper_cut = max(upper - line_padding, 0)
            pt_lower_cut = min(lower + line_padding, H)

            crop_img = get_image_cropped(img, pt_upper_cut, pt_lower_cut)
            slices.append(crop_img.copy())

    return slices


def slice(path_image: str,
          interactive=False,
          save_cropped=False,
          th_pxl_density=DEFAULT_TH_PIXEL_DENSITY,
          line_padding=7):

    filename_image = path_image
    image = cv2.imread(path_image)

    orig = image.copy()
    working_image = image.copy()
    H, W = image.shape[:2]

    working_image = cv2.cvtColor(working_image, cv2.COLOR_BGR2GRAY)

    computed_threshold, working_image = get_inverted_thresholded_image(
        working_image)

    uppers, lowers = get_slices(working_image, th_pxl_density)

    while interactive:

        display_image = orig.copy()

        display_image = draw_slices_on_image(display_image, uppers, lowers, line_padding=line_padding)

        logger.info("Current threshold_pxl_density: " + str(th_pxl_density))
        logger.info("Current threshold_pxl_line: " + str(line_padding) + "\n")

        show_image_normal_window("Lines result", display_image)

        th_pxl_density, line_padding, interactive = handle_interactive_key_input(th_pxl_density, line_padding)

        uppers, lowers = get_slices(working_image, th_pxl_density)

    cv2.destroyAllWindows()

    # Pairing is here after (possible) image display to
    # keep interactive mode transparent.
    uppers, lowers = pair_upper_lower_bounds(uppers, lowers)

    slices = get_slices_as_img_list(orig,
                                upper_bounds=uppers,
                                lower_bounds=lowers,
                                line_padding=line_padding,
                                margin_factor=DEFAULT_CUT_MARGIN_FACTOR)

    if save_cropped:
        parameters_str = str(th_pxl_density) + "_" + str(line_padding)
        path, basename, ext = get_path_base_and_ext(filename_image)
        path_output = path + '/output_cropped/' + basename + "_" + parameters_str
        os.makedirs(path_output, exist_ok=True)

        for slice, upper, lower in zip(slices, uppers, lowers):
            fname = "cropped_" + str(lower) + "_" + str(upper) + ".png"
            cv2.imwrite(path_output + "/" + fname, slice)

        now_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        cv2.imwrite(path_output + "/original_" + now_timestamp + ext, orig)

    return path_output if save_cropped else slices


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-d", "--threshold-pxl-density",
                type=float,
                default=DEFAULT_TH_PIXEL_DENSITY,
                help="Path to the image to be scanned")
ap.add_argument("-p", "--line-padding",
                default=DEFAULT_LINE_PADDING,
                type=int,
                help="Path to the image to be scanned")
ap.add_argument("-I", "--interactive",
                action="store_true",
                default=False,
                help="Slice interactively showing image to modify variables with [ ` . + - ] characters")
ap.add_argument("-S", "--save-cropped",
                action="store_true",
                default=False,
                help="Save cropped images")
ap.add_argument('-v', '--verbose',
                dest="loglevel",
                help="set loglevel to INFO",
                action='store_const',
                const=logging.INFO)
ap.add_argument('-vv', '--very-verbose',
                dest="loglevel",
                help="set loglevel to DEBUG",
                action='store_const',
                const=logging.DEBUG)


if __name__ == "__main__":
    args = vars(ap.parse_args())
    setup_logging(args["loglevel"])

    slice(path_image=args["image"],
          interactive=args["interactive"],
          save_cropped=args["save_cropped"],
          th_pxl_density=args["threshold_pxl_density"],
          line_padding=args["line_padding"]
    )
