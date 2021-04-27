# SPDX-License-Identifier: GPL-3.0-or-later

import logging

LOGGER = logging.getLogger(__name__)


def insert_store(node, cur):
    from comicindex.address import insert_address

    LOGGER.debug('Inserting node ID %d', node.id)

    tags = node.tags
    name = None
    phone_number = None
    email_address = None
    website = None
    lic = 1
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
            (name, phone_number, email_address, website, license, address)
            VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone_number, email_address, website, lic, address))
    return cur.lastrowid
