#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
import os
from gi.repository import Gtk, Gio

import appdirs

from tarpon_app.docsets import Docset
from tarpon_app.gtk.components import TarponWindow, views
import tarpon_app.info as info


APP_MENU = """<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <menu id="menu">
    <section>
        <item>
            <attribute name="label">_New Window</attribute>
            <attribute name="accel">&lt;Primary&gt;n</attribute>
            <attribute name="action">app.new_window</attribute>
        </item>
    </section>
    <section>
        <item>
            <attribute name="label" translatable="yes">Preferences</attribute>
            <attribute name="action">app.preferences</attribute>
        </item>
    </section>
        <section>
            <item>
                <attribute name="label" translatable="yes">About</attribute>
                <attribute name="action">app.about</attribute>
            </item>
            <item>
                <attribute name="label" translatable="yes">_Quit</attribute>
                <attribute name="accel">&lt;Primary&gt;q</attribute>
                <attribute name="action">app.quit</attribute>
            </item>
    </section>
    </menu>
</interface>
"""


def ensure(path):
    """
    Ensures that a path exists by creating it if necessary.

    Note: ``os.makedirs()`` in Python 3 has the option ``exist_ok`` which will
    not throw an error if the directory already exist (making this function
    unnecessary). However, Python 2 has no such option.

    :type path: str
    :param path: path to be created if necessary
    :rtype: str
    :returns: input path (allowing functions like os.path.join to be wrapped)
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


class Application(Gtk.Application):
    data_dir = ensure(appdirs.user_data_dir(appname=info.SHORT_NAME))
    cache_dir = ensure(appdirs.user_cache_dir(appname=info.SHORT_NAME))
    # log_dir = ensure(appdirs.user_log_dir(appname=info.SHORT_NAME))
    docsets = {}

    def __init__(self, package, version, pkgdatadir):
        Gtk.Application.__init__(self, application_id="com.sarkhelk.tarpon",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.package = package
        self.version = version
        self.pkgdatadir = pkgdatadir
        search_paths = glob.glob(self.data_dir + "/*.docset")
        search_paths.extend(glob.glob(self.cache_dir + "/*.json"))
        self.__choices = []
        self.load_docsets(search_paths)

    @property
    def choices(self):
        return self.__choices

    def __new_window(self):
        window = TarponWindow(self)
        window.show_all()
        self.add_window(window)

    def do_activate(self):
        self.__new_window()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        if self.prefers_app_menu():
            print("prefers app_menu")
            builder = Gtk.Builder()
            builder.add_from_string(APP_MENU)
            self.set_app_menu(builder.get_object("menu"))
        else:
            builder = Gtk.Builder()
            print(views(self.pkgdatadir, "menubar.ui"))
            builder.add_from_file(views(self.pkgdatadir, "menubar.ui"))
            self.set_menubar(builder.get_object("menu"))

        new_window_action = Gio.SimpleAction.new("new_window", None)
        new_window_action.connect("activate", self.on_new_window)
        self.add_action(new_window_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

        preferences_action = Gio.SimpleAction.new("preferences", None)
        preferences_action.connect("activate", self.on_preferences)
        self.add_action(preferences_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)

    def load_docsets(self, paths):
        for path in paths:
            if path.endswith(".docset"):  # load from disk
                docset = Docset.frompath(path)
                self.docsets[docset.name] = docset
                self.__choices.extend(docset.items)
            elif path.endswith(".json"):  # load from cache files
                with open(path) as cache_file:
                    for name, url in json.load(cache_file).iteritems():
                        if name in self.docsets:
                            self.docsets[name].url = url
                        else:
                            self.docsets[name] = Docset(name, url=url)

    @property
    def docsets_on_disk(self):
        return filter(lambda x: x[1].on_disk, self.docsets.iteritems())

    def on_new_window(self, action, parameter):
        self.__new_window()

    def on_quit(self, action, parameter):
        self.quit()

    def on_about(self, action, parameter, transient_for=None):
        builder = Gtk.Builder()
        if self.prefers_app_menu():
            builder.add_from_file(views(self.pkgdatadir, "about_dialog_hb.ui"))
        else:
            builder.add_from_file(views(self.pkgdatadir, "about_dialog.ui"))

        about_dialog = builder.get_object("about_dialog")
        if transient_for:
            about_dialog.set_transient_for(transient_for)
        about_dialog.run()
        about_dialog.destroy()

    def on_preferences(self, action, parameter):
        pass
