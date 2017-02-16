#!/usr/bin/env python
from setuptools import setup
import sys
from os.path import normpath, dirname, join


def read_rst(f):
    with open('README.rst') as f:
        return f.read()

README = normpath(join(dirname(__file__), 'README.rst'))

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

setup(name='Office365Api-27',
      version= "0.0.5",
      description='Python library for working with Microsoft Office 365',
      long_description=read_rst(README),
      author='Dmitriy Krasnikov',
      author_email='dmitriy.krasnikov@swimlane.com',
      maintainer='Dmitriy Krasnikov',
      maintainer_email='dmitriy.krasnikov@swimlane.com',
      url='https://github.com/swimlane/python-office365',
      packages=['office365api', 'office365api/model', 'office365api/mail'],
      install_requires=['requests'],
      license='MIT',
      classifiers=CLASSIFIERS
      )
