#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukdbconn.py
# $Date: Thu Dec 12 11:55:37 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""database connections"""

__all__ = ['get_mongo']

import ukconfig

try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient

from pymongo.errors import DuplicateKeyError
from bson.binary import Binary

_db = None


def get_mongo(coll_name=None):
    global _db
    if _db is None:
        _db = MongoClient(*ukconfig.mongo_conn)[ukconfig.mongo_db]

    if coll_name is None:
        return _db
    return _db[coll_name]


def global_counter(name, delta=1):
    """atomically change a global int64 counter and return the newest value;
    starting from 1
    mongo document structure:
    {
        _id: counter name
        val: current value
    }"""
    coll_name = 'global_counter'
    db = get_mongo()
    rst = db.command('findAndModify', coll_name,
                     query={'_id': name},
                     update={'$inc': {'val': delta}},
                     new=True)
    if rst['value']:
        return rst['value']['val']
    try:
        val = long(1)
        db[coll_name].insert({'_id': name, 'val': val})
        return val
    except DuplicateKeyError:
        return global_counter(name, delta)


def get_user(username):
    db = get_mongo('user')
    u = list(db.find({'username': username}).limit(1))
    if len(u) == 0:
        return None
    return u[0]


def declare_general_tag(tags):
    """ declare the existant of a general tag, increment the cnt by 1
    tags: list of string
    {
        _id: 'tagname',
        cnt: integer            # number of items under this tag
    }
    """
    coll_name = 'general_tags'
    db = get_mongo()
    for tag in tags:
        db.command('findAndModify', coll_name,
                   query={'_id': tag},
                   update={'$inc': {'cnt': 1}},
                   new=True)
        try:
            cnt = 1
            db[coll_name].insert({'_id': tag, 'cnt': cnt})
        except DuplicateKeyError:
            pass
