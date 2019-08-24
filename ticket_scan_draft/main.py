import cv2
import argparse
import slice as slicer
import ocr_batch


DEFAULT_SCAN = False

#
# construct the argument parser and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
ap.add_argument("-s", "--scan",
                action="store_true",
                default=DEFAULT_SCAN,
                help="Crop and transform image searching for document form")

if __name__ == "__main__":
    args = vars(ap.parse_args())

    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    path_image = args["image"]

    if args["scan"]:
        pass

    path_output = slicer.slice(path_image, interactive=False)

    ocr_batch.extract_lines_of_text(path_output)
