import unittest
import os
from yamltools import spinnaker
import logging
logger = logging.getLogger(__name__)

settings_js_result = """var gateUrl = "http://mockurl";
var authEnabled = false;
window.spinnakerSettings = {
  gateUrl: gateUrl,
  bakeryDetailUrl: gateUrl + '/bakery/logs/global/{{context.status.id}}',
};
"""

class TestSpinnaker(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        logger.debug("directory is currently: %s", self.dir_path)

    def test_missing_profile_doesnt_throw_exception(self):
        #shouldn't throw an exception if profile doens't exist
        try:
            settings = spinnaker.settings(
                    spinnaker_opt_dir="%s/fixtures" % self.dir_path,
                    spring_profiles_active="somefakeprofile, armory, local")
        except Exception as e:
            logger.exception(e)
            self.fail("settings() failed unexpectedly")

    def test_settings_js_render(self):
        settings_js_path = "%s/fixtures/settings.tpl.js" % self.dir_path
        settings_js_txt = open(settings_js_path).read()
        settings = {
            'services.deck.gateUrl': 'http://mockurl',
            #make sure the false gets casted correctly
            'services.deck.auth.enabled': False
        }

        result = spinnaker.render_deck_settings(settings_js_txt, settings)
        logger.info(result)
        self.assertEquals(settings_js_result, result)

    def test_get_settings(self):
        settings = spinnaker.settings(
                    spinnaker_opt_dir="%s/fixtures" % self.dir_path,
                    spring_profiles_active="armory, local")
        print(settings)
        #make sure the key got overwritten by local
        self.assertEquals(settings["spinnaker.armory"], False)
        #make sure spinnakery main got called
        self.assertEquals(settings["spinnaker.default"], True)
