#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later

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
        'jinja2',
    ],
    scripts=['bin/comicindex']
)
