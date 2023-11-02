#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='continuity',
      version='1.1.0',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'continuity=continuity.main:main'
          ],
      }
     )
