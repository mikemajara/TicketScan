import argparse
import os
import cv2
import json
import natsort
import time
import logging
from typing import List
from ticket_scan.scanner import slicer
from ticket_scan.scanner import ocr
from ticket_scan.scanner.helpers import setup_logging


DEFAULT_OEM = 1
DEFAULT_PSM = 7
DEFAULT_SIDE_MARGIN = 5
DEFAULT_PREFIX_CROPPED = "cropped"
IMAGE_SUPPORTED_EXTENSIONS = ".png"

logger = logging.getLogger(__name__)


def save_dict_to_file(result_path, dictionary):
    with open(result_path,"w") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)


def get_sorted_file_list_for_path(path, prefixes: List[str] = None, suffixes: List[str] = None):
    """
    Returns a sorted list of files for path. If prefixes or suffixes are provided, only those containing any
    of the provided are returned.
    :param path:
    :param prefixes:
    :param suffixes:
    :return:
    """
    file_list = os.listdir(path)
    if prefixes is not None:
        file_list = list(filter(lambda x: any([x.startswith(pref) for pref in prefixes]), file_list))
    if suffixes is not None:
        file_list = list(filter(lambda x: any([x.endswith(suf) for suf in suffixes]), file_list))
    file_list = natsort.natsorted(file_list)
    return file_list


def extract_text_lines_from_path(path,
                                 oem=DEFAULT_OEM,
                                 psm=DEFAULT_PSM,
                                 side_margin=DEFAULT_SIDE_MARGIN,
                                 prefixes: List[str]=None, suffixes: List[str]=None,
                                 *args, **kwargs
                                 ):
    """
    Extracts text from all image files in a given path.
    :param path:
    :param oem:
    :param psm:
    :param side_margin:
    :param file_images_prefix:
    :param args:
    :param kwargs:
    :return:
    """
    text_recognition_dict = {}

    file_list = get_sorted_file_list_for_path(path, prefixes=prefixes, suffixes=suffixes)

    for file in file_list:
        filepath = os.path.join(path, file)
        image = cv2.imread(filepath)
        text_recognition_dict[file] = \
            ocr.extract_text_from_image(
                img=image,
                oem=oem,
                psm=psm,
                lang="spa",
                side_margin=side_margin
            )

    result_path = os.path.join(path, f"text_recognition_{str(oem)}_{str(psm)}.json")
    save_dict_to_file(result_path, text_recognition_dict)

    return text_recognition_dict


def extract_text_lines_from_image(image,
                                  oem=DEFAULT_OEM,
                                  psm=DEFAULT_PSM,
                                  side_margin=DEFAULT_SIDE_MARGIN,
                                  *args, **kwargs
                                  ):
    text_recognition_dict = {}

    start = time.time()
    slices = slicer.slice(image, *args, **kwargs)
    end = time.time()
    logger.info(f"sliced image in {str(end - start)}s")

    start = time.time()
    for idx, slice in enumerate(slices):
        text_recognition_dict[idx] = \
            ocr.extract_text_from_image(
                img=slice,
                oem=oem,
                psm=psm,
                lang="spa",
                side_margin=side_margin
            )
    end = time.time()
    logger.info(f"read slices in {str(end - start)}s")

    image_path = os.path.dirname(image)
    result_path = os.path.join(image_path, 'text_recognition_result.json')
    save_dict_to_file(result_path, text_recognition_dict)

    return text_recognition_dict


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path",
                default=None,
                type=str,
                help="Path to folder with images to be scanned")
ap.add_argument("-i", "--image",
                default=None,
                type=str,
                help="Path to the image to be scanned")
ap.add_argument("-S", "--save-cropped",
                action="store_true",
                default=False,
                help="Save cropped images")
ap.add_argument("-I", "--interactive",
                action="store_true",
                default=False,
                help="Slice interactively showing image to modify variables with [ ` . + - ] characters")
ap.add_argument("-o", "--output-path",
                default='',
                type=str,
                help="Path for the results to be saved")
ap.add_argument("-m", "--side-margin",
                default=DEFAULT_SIDE_MARGIN,
                type=int,
                help="Side margin to crop from image (default " + str(DEFAULT_SIDE_MARGIN) + ")")
ap.add_argument("-oem", "--oem", type=int, default=DEFAULT_OEM,
                help="controls the type of algorithm used by Tesseract."
                     "OCR Engine modes:"
                     "0    Legacy engine only."
                     "1    Neural nets LSTM engine only."
                     "2    Legacy + LSTM engines."
                     "3    Default, based on what is available."
                     "(default " + str(DEFAULT_OEM) + ")"
                )
ap.add_argument("-psm", "--psm", type=int, default=DEFAULT_PSM,
                help="controls the automatic Page Segmentation Mode used by Tesseract"
                     "Page segmentation modes:"
                     "0    Orientation and script detection (OSD) only."
                     "1    Automatic page segmentation with OSD."
                     "2    Automatic page segmentation, but no OSD, or OCR."
                     "3    Fully automatic page segmentation, but no OSD. (Default)"
                     "4    Assume a single column of text of variable sizes."
                     "5    Assume a single uniform block of vertically aligned text."
                     "6    Assume a single uniform block of text."
                     "7    Treat the image as a single text line."
                     "8    Treat the image as a single word."
                     "9    Treat the image as a single word in a circle."
                     "10    Treat the image as a single character."
                     "11    Sparse text. Find as much text as possible in no particular order."
                     "12    Sparse text with OSD."
                     "13    Raw line. Treat the image as a single text line,"
                     "      bypassing hacks that are Tesseract-specific."
                     "(default " + str(DEFAULT_PSM) + ")"
                )
ap.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
ap.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)

if __name__ == "__main__":
    args = vars(ap.parse_args())
    setup_logging(args["loglevel"])

    assert args["path"] is None or os.path.isdir(args["path"])
    assert args["image"] is None or os.path.isfile(args["image"])

    if args["path"] is not None:
        extract_text_lines_from_path(path=args["path"],
                                     oem=args["oem"],
                                     psm=args["psm"],
                                     side_margin=args["side_margin"],
                                     save_cropped=args["save_cropped"],
                                     output_path=args["output_path"],
                                     interactive=args["interactive"]
                                     )
    elif args["image"] is not None:
        extract_text_lines_from_image(image=args["image"],
                                      oem=args["oem"],
                                      psm=args["psm"],
                                      side_margin=args["side_margin"],
                                      save_cropped=args["save_cropped"],
                                      output_path=args["output_path"],
                                      interactive=args["interactive"]
                                      )
    else:
        logger.error("path or image must be provided")