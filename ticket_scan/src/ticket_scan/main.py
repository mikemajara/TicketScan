#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = ticket_scan.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

from ticket_scan import __version__
import argparse
import sys
import logging

from ticket_scan.server import Server
from flask import Flask
from flask_restful import Api

from ticket_scan.scanner import slicer, ocr_batch


DEFAULT_LISTEN = False


__author__ = "Miguel López-N. Alcalde"
__copyright__ = "Miguel López-N. Alcalde"
__license__ = "proprietary"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonnaci demonstration")
    parser.add_argument(
        '--version',
        action='version',
        version='ticket_scan {ver}'.format(ver=__version__))
    parser.add_argument(
        "-i", "--image", required=False,
        help="Path to the image to be scanned")
    parser.add_argument(
        "-l", "--listen",
        action="store_true",
        default=DEFAULT_LISTEN,
        help="Crop and transform image searching for document form")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
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


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Server, '/api')
    return app


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy scanner...")

    path_image = args.image

    if args.listen:
        app = create_app()
        app.run(debug=True)
    elif args.image:
        #path_output = slicer.slice(path_image, interactive=False)
        ocr_batch.extract_text_lines_from_image(image=args.image)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


def listen():
    """Start server
    """
    pass


if __name__ == "__main__":
    run()
