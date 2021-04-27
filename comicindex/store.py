# SPDX-License-Identifier: GPL-3.0-or-later

import logging

LOGGER = logging.getLogger(__name__)


def insert_store(node, cur):
    import json
    from comicindex.address import insert_address, node_id

    LOGGER.debug('Inserting node ID %d', node.id)

    tags = node.tags
    osm_id = node_id(node)
    name = None
    phone_number = None
    email_address = None
    website = None
    lic = 1
    tag_json = json.dumps(tags)
    address = insert_address(node, cur)

    if 'name' in tags:
        name = tags['name']

    if 'phone' in tags:
        phone_number = tags['phone']
    elif 'contact:phone' in tags:
        phone_number = tags['contact:phone']
    elif 'contact:mobile' in tags:
        phone_number = tags['contact:mobile']

    if 'email' in tags:
        email_address = tags['email']
    elif 'contact:email' in tags:
        email_address = tags['contact:email']

    if 'website' in tags:
        website = tags['website']
    elif 'contact:website' in tags:
        website = tags['contact:website']

    cur.execute('''
        INSERT INTO stores
            (osm_id, name, phone_number, email_address, website, license, tags, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (osm_id, name, phone_number, email_address, website, lic, tag_json, address))
    return cur.lastrowid
