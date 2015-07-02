#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import appdirs
import application.info


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


class Application:
    data_dir = ensure(appdirs.user_data_dir(appname=info.SHORT_NAME))
    cache_dir = ensure(appdirs.user_cache_dir(appname=info.SHORT_NAME))
    # log_dir = ensure(appdirs.user_log_dir(appname=info.SHORT_NAME))
