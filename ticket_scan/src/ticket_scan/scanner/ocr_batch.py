import argparse
import os
import cv2
import json
import natsort
import time
import logging
from ticket_scan.scanner import slicer
from ticket_scan.scanner.ocr import extract_text
from ticket_scan.scanner.helpers import setup_logging


DEFAULT_OEM = 1
DEFAULT_PSM = 7
DEFAULT_SIDE_MARGIN = 5
DEFAULT_FULL_BOX_IMAGE = True

logger = logging.getLogger(__name__)

def get_sorted_file_list_for_path(path, prefix=""):
    file_list = os.listdir(path)
    if len(prefix) > 0:
        file_list = list(filter(lambda x: x.startswith(prefix), file_list))
    file_list = natsort.natsorted(file_list)
    return file_list


def extract_text_lines_from_image(path=None,
                                  image=None,
                                  oem=DEFAULT_OEM,
                                  psm=DEFAULT_PSM,
                                  side_margin=DEFAULT_SIDE_MARGIN,
                                  full_box_image=DEFAULT_FULL_BOX_IMAGE,
                                  *args, **kwargs
                                  ):
    text_recognition_dict = {}

    if path is not None:
        file_list = get_sorted_file_list_for_path(path, prefix="cropped")

        for file in file_list:

            if file.startswith("cropped"):
                filepath = os.path.join(path, file)
                print(filepath)
                image = cv2.imread(filepath)
                orig = image.copy()

                text_recognised = extract_text(img=orig,
                                               oem=oem,
                                               psm=psm,
                                               lang="spa",
                                               full_box_image=full_box_image,
                                               side_margin=side_margin)
                text_recognition_dict[file] = text_recognised

        f = open(os.path.join(path, "text_recognition_" +
                              str(oem) + "_" + str(psm) + ".json"), "w")
        json.dump(text_recognition_dict, f, ensure_ascii=False, indent=2)

        f = open(os.path.join(path, "result.json"), "w")
        json.dump(text_recognition_dict, f, ensure_ascii=False, indent=2)

        f.close()

    if image is not None:
        start = time.time()
        slices = slicer.slice(image, *args, **kwargs)
        end = time.time()
        logger.info("sliced image in " + str(end - start) + "s")

        start = time.time()
        for idx, slice in enumerate(slices):
            text_recognised = extract_text(img=slice,
                                           oem=oem,
                                           psm=psm,
                                           lang="spa",
                                           full_box_image=full_box_image,
                                           side_margin=side_margin)
            text_recognition_dict[idx] = text_recognised
        end = time.time()
        logger.info("read slices in " + str(end - start) + "s")

        image_path = os.path.dirname(image)
        result_path = os.path.join(image_path, 'text_recognition_result.json')
        f = open(result_path,"w")
        json.dump(text_recognition_dict, f, ensure_ascii=False, indent=2)
        f.close()

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
ap.add_argument("-f", "--full-box-image",
                action="store_true",
                default=DEFAULT_FULL_BOX_IMAGE,
                help="Take full image as text (default " + str(DEFAULT_FULL_BOX_IMAGE) + ")")
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

    extract_text_lines_from_image(path=args["path"],
                                  image=args["image"],
                                  oem=args["oem"],
                                  psm=args["psm"],
                                  full_box_image=args["full_box_image"],
                                  side_margin=args["side_margin"],
                                  save_cropped=args["save_cropped"],
                                  output_path=args["output_path"],
                                  interactive=args["interactive"]
                                  )
