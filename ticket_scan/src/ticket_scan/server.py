import os
import datetime as dt
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from scanner import slicer, ocr_batch


class Server(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage,
                           location='files')

        args = parse.parse_args()

        file = args['file']
        timestamp = dt.datetime.now().isoformat()
        filext = os.path.splitext(file.filename)[1]
        filepath = '../../uploaded_images/' + timestamp + filext
        file.save(filepath)
        path_output = slicer.slice(filepath, interactive=False)
        result = ocr_batch.extract_lines_of_text(path_output)

        return result
