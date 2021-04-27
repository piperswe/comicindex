# SPDX-License-Identifier: GPL-3.0-or-later

SCHEMA = '''
create table licenses
(
    id      integer not null
        constraint licenses_pk
            primary key autoincrement,
    license text
);

create table addresses
(
    id           integer not null
        constraint addresses_pk
            primary key autoincrement,
    display_name text,
    line_1       text,
    line_2       text,
    city         text,
    region       text,
    postal_code  text,
    country      text,
    nominatim    text,
    license      int
        references licenses
);

create index addresses_city_index
    on addresses (city);

create index addresses_country_region_city_index
    on addresses (country, region, city);

create index addresses_postal_code_index
    on addresses (postal_code);

create index addresses_region_city_index
    on addresses (region, city);

create table stores
(
    id            integer not null
        constraint stores_pk
            primary key autoincrement,
    osm_id        text,
    name          text,
    address       integer
        references addresses,
    phone_number  text,
    email_address text,
    website       text,
    tags          text,
    license       integer
        references licenses
);

create index stores_osm_id_index
    on stores (osm_id);

create index stores_address_index
    on stores (address);

create index stores_name_index
    on stores (name);

insert into licenses (id, license)
values  (1, 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright');
'''

DEFAULT_PATH = 'comic.index'


def get_db(path=DEFAULT_PATH):
    import sqlite3
    db = sqlite3.connect(path)
    db.execute('PRAGMA journal_mode = WAL')
    db.execute('PRAGMA synchronous = normal')
    db.execute('PRAGMA temp_store = memory')
    db.execute('PRAGMA mmap_size = 100000000')
    return db


def get_new_db(path=DEFAULT_PATH):
    import os
    if os.path.exists(path):
        os.remove(path)

    db = get_db(path)
    cur = db.cursor()
    cur.executescript(SCHEMA)
    db.commit()
    return db
