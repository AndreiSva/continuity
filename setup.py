#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='continuity',
      version='0.1',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'continuity=continuity.main:prog_start'
          ],
      }
     )
