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
        environ["SPINNAKER_AWS_ENABLED"] = "is_enabled"
        environ["DEFAULT_DNS_NAME"] = "mockdns.com"
        environ["REDIS_HOST"] = "redishost.com"

        result = resolver.resolve_yamls(
                    [armory_yaml, local_yaml, spinnaker_yaml, environ]
                )
        logger.info(result)
        self.assertEquals(result["providers.aws.enabled"], "is_enabled1")
