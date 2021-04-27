#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
from jinja2 import Template

LOGGER = logging.getLogger(__name__)

QUERY = '''
    (
        node["shop"="books"]["books"="comic"];
        way["shop"="books"]["books"="comic"];
        relation["shop"="books"]["books"="comic"];
    );
    out;
'''

INDEX_TEMPLATE_STR = '''<!DOCTYPE html>
<html>
<head>
    <title>comicindex</title>
</head>
<body>
<h1>comicindex</h1>
<p>last update {{now}}</p>
<ul>
    <li><a href="{{path}}">{{path}}</a></li>
    <li><a href="{{path}}.gz">{{path}}.gz</a></li>
    <li><a href="{{path}}.bz2">{{path}}.bz2</a></li>
    <li><a href="{{path}}.xz">{{path}}.xz</a></li>
    <li><a href="{{path}}.br">{{path}}.br</a></li>
</ul>
</body>
</html>

'''

INDEX_TEMPLATE = Template(INDEX_TEMPLATE_STR)


def init_parser(p):
    p.add_argument('-o', '--out', dest='out', default='docs', help='Output file')


def compress(path):
    import zopfli.gzip as zopfli
    import bz2
    import lzma
    import brotli
    LOGGER.info('Creating compressed versions...')
    with open(path, 'rb') as i:
        d = i.read()
        LOGGER.info('Compressing with zopfli (gzip-compatible)...')
        with open('{}.gz'.format(path), 'wb') as o:
            o.write(zopfli.compress(d))
        LOGGER.info('Compressing with bz2...')
        with open('{}.bz2'.format(path), 'wb') as o:
            o.write(bz2.compress(d))
        LOGGER.info('Compressing with xz...')
        with open('{}.xz'.format(path), 'wb') as o:
            o.write(lzma.compress(d, preset=9 | lzma.PRESET_EXTREME))
        LOGGER.info('Compressing with brotli...')
        with open('{}.br'.format(path), 'wb') as o:
            o.write(brotli.compress(d))


def build(path):
    import os
    from overpy import Overpass
    from datetime import datetime
    from comicindex.address import fetch_addresses
    from comicindex.store import insert_store
    from comicindex.db import get_new_db

    api = Overpass()

    LOGGER.info('Querying OpenStreetMap...')
    result = api.query(QUERY)
    nodes = result.nodes + result.ways + result.relations
    LOGGER.info('Fetching addresses...')
    fetch_addresses(nodes)
    LOGGER.info('Saving to index database...')
    os.makedirs(path, exist_ok=True)
    db = get_new_db(os.path.join(path, 'comic.index'))
    cur = db.cursor()
    for n in nodes:
        insert_store(n, cur)
    db.commit()
    db.execute('VACUUM')
    db.execute('PRAGMA OPTIMIZE')
    db.close()
    compress(os.path.join(path, 'comic.index'))
    with open(os.path.join(path, 'index.html'), 'w') as o:
        o.write(INDEX_TEMPLATE.render(now=str(datetime.now()), path=path))
    LOGGER.info('Successfully built an index of %d stores.', len(nodes))


def main(args):
    build(args.out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_parser(parser)
    parsed = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(parsed)
