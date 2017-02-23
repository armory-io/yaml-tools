import unittest
import os
from yamltools import spinnaker
import logging
logger = logging.getLogger(__name__)

class TestSpinnaker(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        logger.debug("directory is currently: %s", self.dir_path)

    # def test_ordered_loading(self):
    #     fixtures_dir = "%s/fixtures/profiles" % self.dir_path
    #     active_profiles= "armory, local".split(",")
    #     yaml_content = spinnaker.load_ordered_file_paths(active_profiles, fixtures_dir)
    #     expected_content = [
    #         {'spinnaker': {'armory': True}}, {'spinnaker': {'local': True}}
    #     ]
    #     self.assertEquals(yaml_content, "[1]")

    def test_default_settings(self):
        settings = spinnaker.settings(
                    spinnaker_opt_dir="%s/fixtures" % self.dir_path,
                    spring_profiles_active="armory, local")
        print(settings)
        #make sure the key got overwritten by local
        self.assertEquals(settings["spinnaker.armory"], False)
        #make sure spinnakery main got called
        self.assertEquals(settings["spinnaker.default"], True)
