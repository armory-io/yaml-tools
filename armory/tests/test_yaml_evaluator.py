import unittest
import os
import logging
import yaml
from flatdict import FlatDict
from armory.yaml import resolver

logger = logging.getLogger(__name__)

class TestYaml(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        logger.debug("directory is currently: %s", self.dir_path)


    def _open_fixture(self, filename):
        file_path = "%s/fixtures/%s" % (self.dir_path, filename)
        yaml_str = open(file_path).read()
        return yaml.load(yaml_str)

    def test_evaluate(self):
        armory_yaml = self._open_fixture("spinnaker-armory.yml")
        local_yaml = self._open_fixture("spinnaker-local.yml")
        spinnaker_yaml = self._open_fixture("spinnaker.yml")

        environ = os.environ.copy()
        environ["SPINNAKER_AWS_ENABLED"] = "true"
        environ["DEFAULT_DNS_NAME"] = "mockdns.com"
        environ["REDIS_HOST"] = "redishost.com"

        #order matters here
        result = resolver.resolve_yamls(
                    [armory_yaml, local_yaml, spinnaker_yaml, environ]
                )

        logger.info(result)
        #simple replace
        self.assertEquals(result["services.rosco.host"], "mockdns.com")
        self.assertEquals(result["providers.google.enabled"], "false")
        #default when no ENV var is present
        self.assertEquals(result["providers.aws.defaultRegion"], "us-west-2")
        #more complex substitution with urls
        self.assertEquals(result["services.fiat.baseUrl"], "http://mockdns.com:7003")
        #empty url
        self.assertEquals(result["providers.google.primaryCredentials.project"], "")
