import os
import logging
import argparse
from helpers import setup_logging
import ocr_batch


CONSTANT = 'CONSTANT'

logger = logging.getLogger(__name__)


def aux_func():
    pass


def scan_ticket(image, *args, **kwargs):
    results = {}
    for line_padding in [3, 5, 7]:
        for th_pxl_density in [4.5, 5.5, 6.5]:
            results[str(line_padding)] = ocr_batch.extract_text_lines_from_image(
                image=image,
                line_padding=line_padding,
                th_pxl_density=th_pxl_density,
                *args, **kwargs
            )
    return results


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-I", "--interactive",
                action="store_true",
                default=False,
                help="Slice interactively showing image to modify variables with [ ` . + - ] characters")
ap.add_argument("-S", "--save-cropped",
                action="store_true",
                default=False,
                help="Save cropped images")
ap.add_argument("-o", "--output-path",
                default='',
                type=str,
                help="Path for the results to be saved")
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

    scan_ticket(image=args["image"],
                interactive=args["interactive"],
                save_cropped=args["save_cropped"],
                output_path=args["output_path"])
