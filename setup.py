#!/usr/bin/env python

from distutils.core import setup

setup(
    name='comicindex',
    version='0.1',
    packages=['comicindex'],
    install_requires=[
        'overpy',
        'requests',
        'brotli',
        'zopfli',
    ],
    scripts=['bin/comicindex']
)
