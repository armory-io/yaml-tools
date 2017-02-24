from yamltools import resolver
from os import listdir
from os.path import isfile, join
import sys
import os
import glob
import yaml
from collections import OrderedDict

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

    yaml_content = map(lambda f: open(f).read(), active_yaml_filenames)
    loaded_yaml = map(yaml.load, yaml_content)
    resolved_settings = resolver.resolve_yamls(list(loaded_yaml))
    return resolved_settings

def substitute_deck_settings(deck_settings_content, spkr_settings):
    pass

def deck_configure():
    spkr_opt_dir = os.environ.get("SPINNAKER_OPT_DIR", spinnaker_opt_dir)
    settings_path = "%s/config/settings.js" % spkr_opt_dir
    deck_settings_content = open(settings_path).read()
    spkr_settings = settings()
    substitute_deck_settings(deck_settings_content, spkr_settings)
