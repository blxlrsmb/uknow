#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Sat Dec 14 23:52:56 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from ukdbconn import get_mongo, DuplicateKeyError

from importlib import import_module
from pkgutil import walk_packages
from datetime import datetime
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


class MongoDBLRUCache(object):
    """naive LRU cache in mongodb
    doc: {
        _id: key
        v: value
        t: creation time, indexed, expire
    }
    """

    expire_time = None
    coll_name = None

    def __init__(self, expire_time, coll_name):
        self.expire_time = expire_time
        self.coll_name = coll_name

    def get_coll(self):
        return get_mongo(self.coll_name)

    def put(self, key, value):
        coll = self.get_coll()
        coll.save({'_id': key, 'v': value,
                   't': datetime.utcnow()})
        coll.ensure_index('t', expireAfterSeconds=self.expire_time)

    def get(self, key, default=None):
        coll = self.get_coll()
        rst = list(coll.find({'_id': key}))
        if rst:
            coll.update({'_id': key}, {'$set': {'t': datetime.utcnow()}})
            return rst[0]['v']
        return default
