import argparse
import os
import cv2
import json
import natsort
import ocr as tr


DEFAULT_OEM = 1
DEFAULT_PSM = 7
DEFAULT_SIDE_MARGIN = 5
DEFAULT_FULL_BOX_IMAGE = True


def extract_lines_of_text(path,
                          oem=DEFAULT_OEM,
                          psm=DEFAULT_PSM,
                          side_margin=DEFAULT_SIDE_MARGIN,
                          full_box_image=DEFAULT_FULL_BOX_IMAGE):
    text_recognition_dict = {}
    file_list = os.listdir(path)
    file_list = list(filter(lambda x: x.startswith("cropped"), file_list))
    file_list = natsort.natsorted(file_list)
    for file in file_list:

        if file.startswith("cropped"):
            filepath = os.path.join(path, file)
            print(filepath)
            image = cv2.imread(filepath)
            orig = image.copy()

            text_recognised = tr.extract_text(img=orig,
                                              oem=oem,
                                              psm=psm,
                                              lang="spa",
                                              full_box_image=full_box_image,
                                              side_margin=side_margin)
            text_recognition_dict[file] = text_recognised

    f = open(os.path.join(path, "text_recognition_" + str(oem) + "_" + str(psm) + ".json"), "w")
    json.dump(text_recognition_dict, f, ensure_ascii=False, indent=2)
    f.close()


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("path",
                help="Path from which to obtain images to parse")
ap.add_argument("-f", "--full-box-image",
                action="store_true",
                default=DEFAULT_FULL_BOX_IMAGE,
                help="Take full image as text")
ap.add_argument("-m", "--side-margin",
                default=DEFAULT_SIDE_MARGIN,
                type=int,
                help="Side margin to crop from image")
ap.add_argument("-oem", "--oem", type=int, default=1,
                help="controls the type of algorithm used by Tesseract."
                     "OCR Engine modes:"
                     "0    Legacy engine only."
                     "1    Neural nets LSTM engine only."
                     "2    Legacy + LSTM engines."
                     "3    Default, based on what is available.")
ap.add_argument("-psm", "--psm", type=int, default=7,
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
                     "      bypassing hacks that are Tesseract-specific.")

if __name__ == "__main__":
    args = vars(ap.parse_args())

    extract_lines_of_text(args["path"],
                          oem=args["oem"],
                          psm=args["psm"],
                          full_box_image=args["full_box_image"],
                          side_margin=args["side_margin"]
                          )
