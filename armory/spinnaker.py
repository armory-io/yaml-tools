
from armory.yaml import resolver
import sys


def default_settings():
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
