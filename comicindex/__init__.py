#!/usr/bin/env python3

import argparse
import logging

import comicindex.build as build

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    build.init_parser(subparsers.add_parser('build', help='Build a comicindex file from OpenStreetMap'))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.command == 'build':
        build.main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
