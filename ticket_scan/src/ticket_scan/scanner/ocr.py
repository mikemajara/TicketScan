# USAGE
# python ocr.py --east frozen_east_text_detection.pb --image images/example_01.jpg
# python ocr.py --east frozen_east_text_detection.pb --image images/example_04.jpg --padding 0.05

# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2


def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < args["min_confidence"]:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def extract_text_from_file(filepath):
    return pytesseract.image_to_string(filepath)


def extract_text_from_image(img, lang="spa", oem=1, psm=7, side_margin=0):

    (H, W) = img.shape[:2]

    blurred = cv2.GaussianBlur(img, (3, 3), 0)

    # extract the ROI
    # Our ROI is currently all the image (except the side_margin)
    roi = blurred[0:H, 0+side_margin:W-side_margin]

    # Read more at "OpenCV OCR and text recognition with Tesseract" in docs
    config = ("-l " + lang +
              " --oem " + str(oem) +
              " --psm " + str(psm))
    return pytesseract.image_to_string(roi, config=config)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
                help="path to input image")
ap.add_argument("-east", "--east", type=str,
                help="path to input EAST text detector")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
                help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=320,
                help="nearest multiple of 32 for resized width")
ap.add_argument("-e", "--height", type=int, default=320,
                help="nearest multiple of 32 for resized height")
ap.add_argument("-p", "--padding", type=int, default=0,
                help="amount of padding to remove from sides")
ap.add_argument("-l", "--language", type=str, default="spa",
                help="controls the language of the input text")
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

    # load the input image and grab the image dimensions
    image = cv2.imread(args["image"])
    orig = image.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (args["width"], args["height"])
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(args["east"])

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []
    boxes = [[0, 0, origW, origH]]
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * args["padding"])
        dY = int((endY - startY) * args["padding"])

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))

        text = extract_text_from_image(orig, startX, startY, endX, endY,
                                       args["language"],
                                       str(args["oem"]),
                                       str(args["psm"]),
                                       side_margin=args["padding"])

        startX += args["padding"]
        endX -= args["padding"]

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])

    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        print("OCR TEXT")
        print("========")
        print(f"{text}\n")

        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        output = orig.copy()
        cv2.rectangle(output, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(output, text, (startX, startY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        # show the output image
        cv2.imshow("Text Detection", output)
        cv2.waitKey(0)
