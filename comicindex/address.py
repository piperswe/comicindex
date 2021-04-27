# SPDX-License-Identifier: GPL-3.0-or-later

import logging

LOGGER = logging.getLogger(__name__)

NOMINATIM_BATCH_SIZE = 50
NOMINATIM_PER_SECOND = 1


def node_id(node):
    from overpy import Node, Way, Relation
    if isinstance(node, Node):
        return 'N{}'.format(node.id)
    elif isinstance(node, Way):
        return 'W{}'.format(node.id)
    elif isinstance(node, Relation):
        return 'R{}'.format(node.id)
    else:
        return None


def fetch_addresses(nodes):
    from requests import get
    from time import sleep

    for i in range(0, len(nodes), NOMINATIM_BATCH_SIZE):
        batch = nodes[i:i + NOMINATIM_BATCH_SIZE]
        LOGGER.debug('Fetching addresses %d through %d...')
        ids = [node_id(node) for node in batch]
        r = get('https://nominatim.openstreetmap.org/lookup',
                params={
                    'osm_ids': ','.join(ids),
                    'format': 'json',
                },
                headers={
                    'user-agent': 'https://github.com/piperswe/comicindex',
                })
        addresses = r.json()
        for j in range(0, len(batch)):
            batch[j].address = addresses[j]
        sleep(1.0 / NOMINATIM_PER_SECOND)


def get_line_1(address):
    parts = []
    if 'house_number' in address:
        parts.append(address['house_number'])
    if 'road' in address:
        parts.append(address['road'])
    return ' '.join(parts)


def get_line_2(address):
    parts = []
    return ' '.join(parts)


def get_license_id(lic, cur):
    rows = cur.execute('SELECT id FROM licenses WHERE license = ?', (lic,))
    if len(rows) > 0:
        return rows[0][0]
    else:
        cur.execute('INSERT INTO licenses (license) VALUES (?)', (lic,))
        return cur.lastrowid


def insert_address(node, cur):
    if not hasattr(node, 'address') or node.address is None:
        return None

    import json

    o = node.address
    display_name = None
    line_1 = None
    line_2 = None
    city = None
    region = None
    postal_code = None
    country = None
    nominatim = json.dumps(o)
    lic = 1

    if 'display_name' in o:
        display_name = o['display_name']

    if 'address' in o:
        addr = o['address']
        line_1 = get_line_1(addr)
        line_2 = get_line_2(addr)
        if 'city' in addr:
            city = addr['city']
        elif 'town' in addr:
            city = addr['town']
        if 'state' in addr:
            region = addr['state']
        elif 'province' in addr:
            region = addr['province']
        if 'postcode' in addr:
            postal_code = addr['postcode']
        if 'country' in addr:
            country = addr['country']

    if 'license' in o:
        lic = get_license_id(o['license'], cur)

    cur.execute('''
        INSERT INTO addresses
            (display_name, line_1, line_2, city, region, postal_code, country, nominatim, license)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (display_name, line_1, line_2, city, region, postal_code, country, nominatim, lic))
    return cur.lastrowid
