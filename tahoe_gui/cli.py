#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from tahoe_gui import __doc__ as description
from tahoe_gui._version import __version__
from tahoe_gui.core import Core


def main():
    parser = argparse.ArgumentParser(
        description=description,
        epilog='Example: %(prog)s <URI>')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug messages to STDOUT.')
    parser.add_argument(
        '-V',
        '--version',
        action="version",
        version='%(prog)s ' + __version__)
    args = parser.parse_args()

    gui = Core(args)
    gui.start()


if __name__ == "__main__":
    sys.exit(main())
