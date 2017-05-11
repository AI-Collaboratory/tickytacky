#!/usr/bin/env python
"""TickyTacky creates metrics for matching the vertical and horizontal lines in an image."""
import logging
from pyclowder.extractors import Extractor
import pyclowder.files
from tickytacky import process


class TickyTackyExtractor(Extractor):
    """Uses OpenCV to find vertical and horizontal lines, then computes metrics."""
    def __init__(self):
        Extractor.__init__(self)

        # add any additional arguments to parser
        # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
        #                          help='maximum number (default=-1)')

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    def process_message(self, connector, host, secret_key, resource, parameters):
        logger = logging.getLogger(__name__)

        inputfile = resource["local_paths"][0]
        file_id = resource['id']
        logger.info("Got a process_file request: "+inputfile)

        (horiz_line_offsets, vertical_line_offsets, height, width) = process(inputfile)

        result = {}  # assertions about the file
        if vertical_line_offsets is not None:
            result['vertical_lines'] = vertical_line_offsets
        if horiz_line_offsets is not None:
            result['horizontal_lines'] = horiz_line_offsets

        metadata = self.get_metadata(result, 'file', file_id, host)

        # upload metadata (metadata is a JSON-LD array of dict)
        pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)


if __name__ == "__main__":
    extractor = TickyTackyExtractor()
    extractor.start()
