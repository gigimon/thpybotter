__author__ = 'gigimon'

import sys
import logging

LOG = logging.getLogger('thpybotter')


def initialize():
    filename = "thbotter.log"
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stderr,
        filename=filename,
        level=logging.DEBUG
    )
    logging.captureWarnings(True)
    LOG.info("Logging initialize...")

initialize()