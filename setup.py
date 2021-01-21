#!/usr/bin/env python

from distutils.core import setup

setup(name='rssconsole',
      version='1.0',
      description='RSS feed reader in Console',
      author='fanfreak247',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['rssconsole'],
      install_requires=[
          'prettytable>=2.0.0',
          'feedparser>=6.0.2',
          'delorean>=2.9.0',
          'google-api-client>=1.12.8'
      ]
     )