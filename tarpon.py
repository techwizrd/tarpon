#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

from application import Application


def main():
    """Starts the Tarpon application"""
    app = Application()
    app.new_window()
    Gtk.main()


if __name__ == '__main__':
    main()
