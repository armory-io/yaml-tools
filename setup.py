#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='yaml-tools',
      version='0.1',
      description='Armory tools for yaml files',
      author='Isaac Mosquera',
      author_email='isaac@armory.io',
      packages=find_packages(),
      install_requires=[
          'pyyaml',
          'nose',
          'flatdict',
          'jinja2'
      ],
      entry_points= {
       "console_scripts": [
            "deck-configure = yamltools.spinnaker:deck_configure"
        ]
      }
)
