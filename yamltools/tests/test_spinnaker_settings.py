import unittest
import os
from yamltools import spinnaker
import logging
logger = logging.getLogger(__name__)

class TestSpinnaker(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        logger.debug("directory is currently: %s", self.dir_path)


    def test_default_settings(self):
        settings = spinnaker.settings()
