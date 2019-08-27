# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = ticket_store.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging

from ticket_store import __version__

__author__ = "Miguel López-N. Alcalde"
__copyright__ = "Miguel López-N. Alcalde"
__license__ = "proprietary"

_logger = logging.getLogger(__name__)

from flask import Flask, request
from flask_pymongo import PyMongo, ObjectId
import json

DEFAULT_LISTEN = True

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="ticket_store {ver}".format(ver=__version__))
    parser.add_argument(
        "-l", "--listen",
        action="store_true",
        default=DEFAULT_LISTEN,
        help="Crop and transform image searching for document form")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")





def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.listen:
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/Tickets"
        mongo = PyMongo(app)

        @app.route("/health", methods=['GET'])
        def health():
            return "ok"

        @app.route("/add_ticket", methods=['POST'])
        def add_ticket():
            j = request.get_json()
            _id = mongo.db.tickets.insert_one(j.get('ticket')).inserted_id
            return {'msg':'ok','_id': str(_id)}

        @app.route("/get_all_tickets", methods=['GET'])
        def get_all_tickets():
            tickets = mongo.db.tickets.find({});
            return { 'tickets': json.loads(json.dumps([ticket for ticket in tickets], default=str))}

        @app.route("/get_ticket/<id>", methods=['GET'])
        def get_ticket(id):
            ticket = mongo.db.tickets.find_one(ObjectId(id))
            return json.loads(json.dumps(ticket, default=str))

        @app.route("/delete_ticket/<id>", methods=['GET'])
        def delete_ticket(id):
            _id = mongo.db.tickets.delete_one({"_id": ObjectId(id)})
            return str(_id)

        app.run(port=5001)
    else:
        _logger.info('App only meant to listen')

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
