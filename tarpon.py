#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from application import Application


def main():
    """Starts the Tarpon application"""
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
