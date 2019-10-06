import os
import cv2
import numpy as np
import datetime as dt
import logging

from flask import jsonify
from flask_restful import Resource, reqparse
from scanner.mercadona_ticket_parser import MercadonaTicketParser
from werkzeug.datastructures import FileStorage

from ticket_scan.scanner import ocr_batch
from ticket_scan.scanner.lidl_ticket_parser import LidlTicketParser

logger = logging.getLogger(__name__)

class Server(Resource):

    UPLOADED_IMAGES_PATH = "../../uploaded_images"
    FILEPATH_FORMAT = UPLOADED_IMAGES_PATH + "/{hash}.{file_extension}"

    def __init__(self):
        os.makedirs(Server.UPLOADED_IMAGES_PATH, exist_ok=True)

    def _dhash(self, file, hash_size = 8):
        # resize the input image, adding a single column (width) so we
        # can compute the horizontal gradient
        resized = cv2.resize(file, (hash_size + 1, hash_size))

        # compute the (relative) horizontal gradient between adjacent
        # column pixels
        diff = resized[:, 1:] > resized[:, :-1]

        # convert the difference image to a hash
        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    def _get_hash(self, file):
        # file is read as an image through numpy to avoid saving it to disk
        # read image file string data
        filestr = file.read()
        # file object’s position needs to point to the 0th byte, otherwise it cannot be saved later on
        file.seek(0)
        # convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if image is None:
            raise Exception("Non existing file: ", file)

        image_blk_white = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_hash = self._dhash(image_blk_white)
        return image_hash

    def _get_filepath(self, file):
        file_extension = file.content_type.split("/")[1]
        filehash = self._get_hash(file)
        filepath = Server.FILEPATH_FORMAT.format(hash=filehash, file_extension=file_extension)
        return os.path.abspath(filepath)

    def save_file(self, file):
        filepath = self._get_filepath(file)
        if not os.path.exists(filepath):
            file.save(filepath)
            logger.info("New file saved: {}".format(filepath))
        else:
            logger.info("Files already exists: {}".format(filepath))
        return filepath

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage,
                           location='files')

        args = parse.parse_args()
        file = args['file']

        result = None
        if file:
            filepath = self.save_file(file)
            # TODO: Implemente a dynamic way to instantiate the parser.
            #ticket_parser = LidlTicketParser()
            ticket_parser = MercadonaTicketParser()
            result = ocr_batch.extract_text_lines_from_image(image=filepath, slicer_options=ticket_parser.slicer_options)
            result = ticket_parser.parse(result)
        else:
            raise Exception("file is None")

        return jsonify(result) if result else {'msg': 'ok'}
