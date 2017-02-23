from yamltools import resolver
from os import listdir
from os.path import isfile, join
import sys
import os
import glob
import yaml
from collections import OrderedDict

def _order_path():
    pass

def settings(spinnaker_opt_dir="/opt/spinnaker/",spring_profiles_active="local"):
    #make some assumptions about the environment
    spkr_opt_dir = os.environ.get("SPINNAKER_OPT_DIR", spinnaker_opt_dir)
    spring_profiles_active = os.environ.get(
                                "SPRING_PROFILES_ACTIVE",
                                spring_profiles_active)

    active_profiles = reversed(spring_profiles_active.split(","))
    ordered_files = OrderedDict()
    for profile in active_profiles:
        ordered_yaml_paths = glob.glob("%s/*-%s.yml" % (spkr_opt_dir, profile))
        for yaml_path in ordered_yaml_paths:
            ordered_files[yaml_path]: open(yaml_path).read()

    paths = OrderedDict()

    return {
        'providers.aws.primaryCredentials.name': 'default-aws-account',
        'providers.aws.defaultIAMRole': 'SpinnakerInstanceProfile',
        'providers.aws.defaultKeyPairTemplate': 'armory-spinnaker-keypair',
        'providers.aws.defaultRegion': 'us-west-2'
    }

def configure_main():
    settings_file = sys.argv[0]
    yaml_templates = sys.argv[1:]
    print(settings_file)
    print(yaml_templates)

def __main__():
    configure_main()
