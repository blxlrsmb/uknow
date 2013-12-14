#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Sat Dec 14 18:00:41 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from ukdbconn import get_mongo, DuplicateKeyError
import time


def get_db_coll():
    return get_mongo('ukfetcher_user_config')


def insert_db_item(user_id, set_name, item_name):
    """insert an item into a set in mongodb"""
    coll = get_db_coll()
    try:
        coll.insert({'_id': user_id, set_name: [item_name]})
    except DuplicateKeyError:
        coll.update({'_id': user_id}, {'$addToSet': {set_name: item_name}})


def remove_db_item(user_id, set_name, item_name):
    get_db_coll().update({'_id': user_id}, {'$pull': {set_name: item_name}})


def get_db_set(user_id, set_name):
    rst = list(get_db_coll().find({'_id': user_id}))
    if rst:
        return rst[0].get(set_name, [])
    return []
