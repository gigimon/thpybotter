__author__ = 'gigimon'

import os
import sys
import logging

LOG = logging.getLogger('thpybotter')


def initialize():
    filename = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'thbotter.log')
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename=filename,
        level=logging.DEBUG,
    )
    logging.captureWarnings(True)
    LOG.info("Logging initialize...")

initialize()