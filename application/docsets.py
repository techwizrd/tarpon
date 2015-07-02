#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import os
import plistlib
from unicodedata import normalize

import peewee


class InvalidDocsetException(Exception):
    pass


DocItem = namedtuple("DocItem", ["name", "data_type", "path"])


def index_model(db):
    class SearchIndex(peewee.Model):
        name = peewee.TextField()
        data_type = peewee.TextField(db_column="type")
        path = peewee.TextField()

        @property
        def item(self):
            return DocItem(normalize("NFKD", unicode(self.name)),
                           str(self.data_type), str(self.path))

        def __str__(self):
            return str(self.item)

        class Meta:
            db_table = "searchIndex"
            database = db

    return SearchIndex


class Docset:
    def __init__(self, name, url=None, path=None):
        self.name = name
        self.url = url
        self.path = path
        self.identifier = None
        self.index_path = None
        self.icon_url = None
        self.icon_path = None
        self._items = None

    @property
    def on_disk(self):
        return self.path and os.path.exists(self.path)

    @property
    def db_path(self):
        if self.on_disk:
            return os.path.join(self.path, "Contents/Resources/docSet.dsidx")

    @property
    def items(self):
        if not self._items:
            db = peewee.SqliteDatabase(self.db_path, threadlocals=True)
            db.connect()
            self._items = [a.item for a in index_model(db).select()]
            db.close()
        return self._items

    def read_docset(self):
        if self.on_disk:
            plist_path = os.path.join(self.path, "Contents", "Info.plist")
            if os.path.exists(plist_path):
                pl = plistlib.readPlist(plist_path)
                if pl["isDashDocset"]:
                    self.name = pl["CFBundleName"]
                    self.identifier = pl["CFBundleIdentifier"]
                    self.index_path = os.path.join(self.path,
                                                   pl["dashIndexFilePath"])
                else:
                    InvalidDocsetException(
                        "isDashDocset is not True in {0}".format(plist_path))
            else:
                raise InvalidDocsetException("{0} not found".format(plist_path))
        else:
            raise InvalidDocsetException("Docset is not on disk")

    def __str__(self):
        return "<Docset '{0}'>".format(self.name)

    @classmethod
    def frompath(cls, path):
        plist_path = os.path.join(path, "Contents", "Info.plist")
        if os.path.exists(plist_path):
            pl = plistlib.readPlist(plist_path)
            if pl["isDashDocset"]:
                new_docset = cls(pl["CFBundleName"], path=path)
                return new_docset
            else:
                InvalidDocsetException(
                    "isDashDocset is not True in {0}".format(plist_path))
        else:
            raise InvalidDocsetException("{0} not found".format(plist_path))
