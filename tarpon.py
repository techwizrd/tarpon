#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tarpon_app.application import Application


def main():
    """Starts the Tarpon application"""
    app = Application(package="tarpon", version="0 (debug)",
                      pkgdatadir=os.path.join(os.path.dirname(__file__),
                                              'data'))
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
