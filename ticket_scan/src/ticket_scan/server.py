import os
import datetime as dt

from flask import jsonify
from flask_restful import Resource, reqparse
from scanner.mercadona_ticket_parser import MercadonaTicketParser
from werkzeug.datastructures import FileStorage

from ticket_scan.scanner import ocr_batch
from ticket_scan.scanner.lidl_ticket_parser import LidlTicketParser


class Server(Resource):

    UPLOADED_IMAGES_PATH = "../../uploaded_images"
    FILEPATH_FORMAT = UPLOADED_IMAGES_PATH + "/{timestamp}.{file_extension}"

    def __init__(self):
        os.makedirs(Server.UPLOADED_IMAGES_PATH, exist_ok=True)

    def _get_filepath(self, file):
        timestamp = dt.datetime.now().isoformat()
        file_extension = file.content_type.split("/")[1]
        filepath = Server.FILEPATH_FORMAT.format(timestamp=timestamp, file_extension=file_extension)
        return filepath

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage,
                           location='files')

        args = parse.parse_args()
        file = args['file']

        result = None
        if file:
            filepath = self._get_filepath(file)
            file.save(filepath)
            # TODO: Implemente a dynamic way to instantiate the parser.
            #ticket_parser = LidlTicketParser()
            ticket_parser = MercadonaTicketParser()
            result = ocr_batch.extract_text_lines_from_image(image=filepath, slicer_options=ticket_parser.slicer_options)
            result = ticket_parser.parse(result)
        else:
            raise Exception("file is None")

        return jsonify(result) if result else {'msg': 'ok'}
