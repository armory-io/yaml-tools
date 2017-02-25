from yamltools import resolver
from os import listdir
from os.path import isfile, join
import sys
import logging
import os
import glob
import yaml
import re
from collections import OrderedDict
logger = logging.getLogger(__name__)

def _read_file_safe(file_path):
    try:
        return open(file_path).read()
    except OSError as e:
        logger.warn("Couldn't open file at path: %s" % file_path)
        logger.warn("This might be okay if you didn't expect that profile to exist")
    return None

def settings(spinnaker_opt_dir="/opt/spinnaker/",spring_profiles_active="local"):
    #make some assumptions about the environment
    spkr_opt_dir = os.environ.get("SPINNAKER_OPT_DIR", spinnaker_opt_dir)
    spring_profiles_active = os.environ.get(
                        "SPRING_PROFILES_ACTIVE",
                        spring_profiles_active)
    spkr_conf_dir = "%s/config" % spkr_opt_dir
    #order them the right way so we overwrite properties properly
    spring_profiles = reversed(spring_profiles_active.split(","))
    #remove extra spaces if any
    profiles_clean = map(lambda p: p.strip(), spring_profiles)
    profile_suffixes = list(map(lambda ps: "-%s" % ps, profiles_clean))
    #we need to add the default profiles, i.e spinnaker.yml
    profile_suffixes.append("")
    active_yaml_filenames = map(
                        lambda p: "%s/spinnaker%s.yml" % (spkr_conf_dir, p),
                        profile_suffixes)

    yaml_content = map(_read_file_safe, active_yaml_filenames)
    nonempty_yamls = filter(lambda f: f is not None, yaml_content)
    loaded_yaml = map(yaml.load, nonempty_yamls)
    resolved_settings = resolver.resolve_yamls(list(loaded_yaml))
    return resolved_settings

def render_deck_settings(deck_settings_txt, spkr_settings):
    keys_to_resolve = re.findall("\$\{(.*?)\}", deck_settings_txt)
    rendered_settings = deck_settings_txt
    for key in keys_to_resolve:
        rendered_settings = rendered_settings.replace(
                    "${%s}" % key,
                    str(spkr_settings.get(key, ''))
                )
    return rendered_settings

def deck_configure():
    spkr_opt_dir = os.environ.get("SPINNAKER_OPT_DIR", "/opt/spinnaker/")
    deck_dir = os.environ.get("DECK_OPT_DIR", "/opt/deck/html")
    logger.info("Using spinnaker directory: %s" % spkr_opt_dir)
    settings_path = "%s/config/settings.js" % spkr_opt_dir
    logger.info("Using settings path: %s" % settings_path)
    deck_settings_content = open(settings_path).read()
    spkr_settings = settings()
    rendered_settings = render_deck_settings(deck_settings_content, spkr_settings)
    logger.info("Writing to file path")
    settings_js_file = open("%s/settings.js" % deck_dir, "w+")
    settings_js_file.write(rendered_settings)
    logger.warn("Completed rendering of deck settings")
