#!/usr/bin/env python
from setuptools import setup
import sys
from os.path import normpath, dirname, join

sys.path.insert(0, normpath(dirname(__file__)))
from office365api import __version__ as _version

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')
except ImportError:
    convert = None
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r').read()   # noqa

README = normpath(join(dirname(__file__), 'README.md'))

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

long_desc = ''

setup(name='Office365Api',
      version=_version,
      description='Python library for working with Microsoft Office 365',
      long_description=read_md(README),
      author='Dmitriy Krasnikov',
      author_email='dmitriy.krasnikov@swimlane.com',
      maintainer='Dmitriy Krasnikov',
      maintainer_email='dmitriy.krasnikov@swimlane.com',
      url='https://github.com/swimlane/python-office365',
      packages=['office365api', 'office365api/model', 'office365api/mail'],
      install_requires=['requests'],
      license='Apache 2.0',
      classifiers=CLASSIFIERS
      )
