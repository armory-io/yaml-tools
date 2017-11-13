from yamltools import resolver
from os import listdir
from os.path import isfile, join
import sys
import logging
import os
import glob
import yaml
import re
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)


def _read_file_safe(file_path):
    try:
        return open(file_path).read()
    except OSError as e:
        logger.warn("Couldn't open file at path: %s" % file_path)
        logger.warn("This might be okay if you didn't expect that profile to exist")
    return None


__settings_cache = None


def settings_cache(spinnaker_config_dir="/opt/spinnaker/config", spring_profiles_active="local"):
    if __settings_cache is None:
        __settings_cache = settings(spinnaker_config_dir, spring_profiles_active)
    return __settings_cache


def settings(spinnaker_config_dir="/opt/spinnaker/config", spring_profiles_active="local"):
    return named_settings(spinnaker_config_dir, spring_profiles_active)


def named_settings(spinnaker_config_dir="/opt/spinnaker/config", spring_profiles_active="local", config_name="spinnaker"):
    # make some assumptions about the environment
    spring_profiles_active = os.environ.get("SPRING_PROFILES_ACTIVE", spring_profiles_active)

    # order them the right way so we overwrite properties properly
    spring_profiles = reversed(spring_profiles_active.split(","))

    # remove extra spaces if any
    profiles_clean = map(lambda p: p.strip(), spring_profiles)
    profile_suffixes = list(map(lambda ps: "-%s" % ps, profiles_clean))

    # we need to add the default profiles, i.e spinnaker.yml
    profile_suffixes.append("")
    active_yaml_filenames = map(lambda p: "%s/%s%s.yml" % (spinnaker_config_dir, config_name, p), profile_suffixes)

    yaml_content = map(_read_file_safe, active_yaml_filenames)
    nonempty_yamls = filter(lambda f: f is not None, yaml_content)
    loaded_yaml = map(yaml.load, nonempty_yamls)
    resolved_settings = resolver.resolve_yamls(list(loaded_yaml))
    return resolved_settings


def render_deck_settings(deck_settings_txt, spkr_settings):
    keys_to_resolve = re.findall("\$\{(.*?)\}", deck_settings_txt)
    rendered_settings = deck_settings_txt
    for key in keys_to_resolve:
        value = spkr_settings.get(key, '')
        value_is_string = isinstance(value, str)

        if value == False or (value_is_string and value.lower() == 'false'):
            print("yml false for:", "${%s}" % key)
            rendered_settings = rendered_settings.replace("${%s}" % key, "false")
        elif value == True or (value_is_string and value.lower() == 'true'):
            print("yml true for:", "${%s}" % key)
            rendered_settings = rendered_settings.replace("${%s}" % key, "true")
        elif value is None or value == '':
            print("yml empty string for:", "${%s}" % key)
            rendered_settings = rendered_settings.replace("${%s}" % key, '')
        else:
            print("yml value for:", "${%s}" % key, str(value))
            rendered_settings = rendered_settings.replace("${%s}" % key, str(value))

    return rendered_settings


def deck_configure():
    deck_dir = os.environ.get("DECK_OPT_DIR", "/opt/deck/html")
    spinnaker_config_dir = os.environ.get("SPINNAKER_CONFIG_DIR", "/opt/spinnaker/config")

    settings_template_path = "%s/settings-template.js" % deck_dir

    logger.info("Path to settings.js template: %s" % settings_template_path)

    deck_settings_content = open(settings_template_path).read()
    spkr_settings = settings(spinnaker_config_dir)
    rendered_settings = render_deck_settings(deck_settings_content, spkr_settings)

    settings_js_rendered = "%s/settings.js" % deck_dir
    logger.info("Writing rendered settings.js to: %s" % settings_js_rendered)

    settings_js_file = open(settings_js_rendered, "w+")
    settings_js_file.write(rendered_settings)
    logger.warn("Completed rendering of deck settings")
