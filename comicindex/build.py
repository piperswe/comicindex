#!/usr/bin/env python3

import argparse
import logging

LOGGER = logging.getLogger(__name__)

QUERY = '''
    node["shop"="books"]["books"="comic"];
    out;
'''


def init_parser(p):
    p.add_argument('-o', '--out', dest='out', default='comic.index', help='Output file')


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
    from overpy import Overpass
    from comicindex.address import fetch_addresses
    from comicindex.store import insert_store
    from comicindex.db import get_new_db

    api = Overpass()

    LOGGER.info('Querying OpenStreetMap...')
    result = api.query(QUERY)
    nodes = result.nodes
    LOGGER.info('Fetching addresses...')
    fetch_addresses(nodes)
    LOGGER.info('Saving to index database...')
    db = get_new_db(path)
    cur = db.cursor()
    for n in nodes:
        insert_store(n, cur)
    db.commit()
    db.execute('VACUUM')
    db.execute('PRAGMA OPTIMIZE')
    db.close()
    compress(path)
    LOGGER.info('Successfully built an index of %d stores.', len(nodes))


def main(args):
    build(args.out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_parser(parser)
    parsed = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(parsed)
