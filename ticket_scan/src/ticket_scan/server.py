import os
from base_ticket_parser import BaseTicketParser
from mercadona_ticket_parser import MercadonaTicketParser
import datetime as dt
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from ticket_scan.scanner import slicer, ocr_batch
from flask import jsonify


class Server(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage,
                           location='files')

        args = parse.parse_args()

        file = args['file']
        result = None
        if file:
            timestamp = dt.datetime.now().isoformat()
            #filext = os.path.splitext(file.filename)[1]
            filext = file.content_type.split("/")[1]
            filepath = '../../uploaded_images/' + timestamp + "." + filext
            file.save(filepath)
            #path_output = slicer.slice(filepath, interactive=False)
            result = ocr_batch.extract_text_lines_from_image(image=filepath)
            ticket_parser = MercadonaTicketParser()
            result = ticket_parser.parse(result)
        else:
            raise Exception("file is None")

        return jsonify(result) if result else {'msg': 'ok'}
