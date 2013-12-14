#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Sat Dec 14 19:13:34 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from ukdbconn import get_mongo, DuplicateKeyError

from importlib import import_module
from pkgutil import walk_packages
import os


def ensure_unicode(s):
    """assert type of s is basestring and convert s to unicode"""
    assert isinstance(s, basestring), 's should be string'
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s


def import_all_modules(file_path, pkg_name):
    """import all modules recursively in a package
    :param file_path: just pass __file__
    :param pkg_name: just pass __name__
    """
    for _, module_name, _ in walk_packages(
            [os.path.dirname(file_path)], pkg_name + '.'):
        import_module(module_name)


def is_in_unittest():
    """return whether currently in unittest mode"""
    return os.getenv('IN_UKNOW_TEST') is not None


class MongoDBSet(object):
    """mantain a set in mongo db"""

    collection_name = None

    def __init__(self, collection_name):
        self.collection_name = collection_name

    def get_coll(self):
        return get_mongo(self.collection_name)

    def add(self, set_name, item):
        coll = self.get_coll()
        try:
            coll.insert({'_id': set_name, 'v': [item]})
        except DuplicateKeyError:
            coll.update({'_id': set_name}, {'$addToSet': {'v': item}})

    def remove(self, set_name, item):
        self.get_coll().update({'_id': set_name}, {'$pull': {'v': item}})

    def get(self, set_name):
        """:return: list of items in this set"""
        rst = list(self.get_coll().find({'_id': set_name}))
        if rst:
            return list(rst[0]['v'])
        return []
