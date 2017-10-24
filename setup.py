#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='RCPU',
      version='0.0.1',
      description='A CPU emulator and assembler.',
      author='redfast00',
      author_email='redfast00@gmail.com',
      url='https://github.com/redfast00/RCPU',
      packages=find_packages(exclude=('tests.*', 'tests',)),
      entry_points={
          'console_scripts': [
              'rcpu_assemble = RCPU.assemble:main',
              'rcpu_emulate = RCPU.emulate:main'
          ]
      }
      )
